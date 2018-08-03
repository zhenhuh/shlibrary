from flask import Flask, request

app = Flask('Yunan Products')

def get_port():
    with open(r"conf\port") as f:
        return int(f.readline())

port_conf = get_port()

def run(debug_mode = False):
    app.run(host = "0.0.0.0", port = port_conf, debug = debug_mode)