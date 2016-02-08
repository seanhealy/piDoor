from flask import Flask
from time import sleep

import pifacedigitalio
import json
import sys

DOOR_PULSE = 0.25  # seconds

try:
    config = json.loads(open("config.json").read())
except:
    print "`config.json` is invalid or doesn't exist."
    sys.exit(1)

DOOR_PULSE = config["door_pulse"]

def toggle_door(id):
    pifacedigital.leds[id].turn_on()
    pifacedigital.relays[id].turn_on()
    sleep(DOOR_PULSE)
    pifacedigital.leds[id].turn_off()
    pifacedigital.relays[id].turn_off()

    return "Toggled Door: {0}".format(id)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/door/<door_id>/toggle")
def toggle(door_id):
    if "0" in config["doors"] and  door_id == config["doors"]["0"]["id"]:
        return toggle_door(0)

    if "1" in config["doors"] and door_id == config["doors"]["1"]["id"]:
        return toggle_door(1)

    return "Unknown Door: {0}".format(door_id)

if __name__ == "__main__":
    pifacedigital = pifacedigitalio.PiFaceDigital()
    # pifacedigital.leds[7].turn_on()

    app.run(host='0.0.0.0', port=8000, debug=True)