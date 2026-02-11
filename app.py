from flask import Flask, jsonify, send_from_directory
import requests, time

app = Flask(__name__)

URL = "https://sistemaintegraloperativo.conavi.gob.mx:9090/Levantamiento/PVB"

@app.route("/status")
def status():
    up = False
    try:
        r = requests.get(URL, timeout=5, verify=False)
        if r.status_code == 200:
            up = True
    except:
        pass

    return jsonify({"up": up, "time": time.strftime("%Y-%m-%d %H:%M:%S")})

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# 👇 MUY IMPORTANTE PARA RENDER
import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
