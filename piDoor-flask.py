from flask import Flask, request
from time import sleep

import pifacedigitalio
import json
import sys

config = json.loads(open("config.json").read())
pifacedigital = pifacedigitalio.PiFaceDigital()

def toggle_door(id):
    pifacedigital.leds[id].turn_on()
    pifacedigital.relays[id].turn_on()
    sleep(config["door_pulse"])
    pifacedigital.leds[id].turn_off()
    pifacedigital.relays[id].turn_off()

    return "Toggled Door: {0}".format(id)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/door/<door_id>/toggle", methods=["PUT"])
def toggle(door_id):
    json = request.get_json()
    key = json["key"]

    if door_id in config["doors"] and config["doors"][door_id]["key"] == key:
        return toggle_door(int(door_id))

    return "Unknown Door: {0}".format(door_id)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2021, debug=True)
