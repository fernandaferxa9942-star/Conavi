from flask import Flask, jsonify, send_from_directory
import requests, time, os

app = Flask(__name__)

# CURP a monitorear
CURP = "MAEP881213HDFRLL09"
# Endpoint que falla 500 hasta que levante
URL = f"https://sistemaintegraloperativo.conavi.gob.mx:9090/Levantamiento/PVB/ValidarCurp?curp={CURP}"

STATUS_FILE = "status.json"

def check_curp():
    """Verifica si la CURP ya responde correctamente"""
    up = False
    try:
        r = requests.get(URL, timeout=5, verify=False)
        if r.status_code != 500:
            up = True
    except:
        pass
    return up

def update_status():
    """Actualiza status.json con estado y hora"""
    status = {
        "curp_responde": check_curp(),
        "hora": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(STATUS_FILE, "w") as f:
        import json
        json.dump(status, f)

# Ruta JSON para la web
@app.route("/status")
def status():
    if os.path.exists(STATUS_FILE):
        import json
        with open(STATUS_FILE, "r") as f:
            data = json.load(f)
        return jsonify(data)
    else:
        return jsonify({"curp_responde": False, "hora": "sin datos"})

# Ruta web
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# 👇 Modo Render: puerto dinámico
if __name__ == "__main__":
    import threading

    # Worker background que revisa CURP cada 30s
    def worker():
        while True:
            update_status()
            time.sleep(30)

    t = threading.Thread(target=worker, daemon=True)
    t.start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
