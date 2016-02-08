from flask import Flask
from time import sleep
import pifacedigitalio

DOOR_PULSE = 0.25  # seconds

def toggle_door():
    pifacedigital.leds[0].turn_on()
    pifacedigital.relays[0].turn_on()
    sleep(DOOR_PULSE)
    pifacedigital.leds[0].turn_off()
    pifacedigital.relays[0].turn_off()
    return

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/toggle")
def toggle():
    toggle_door()
    return "true"

if __name__ == "__main__":
    pifacedigital = pifacedigitalio.PiFaceDigital()
    pifacedigital.leds[7].turn_on()

    app.run(host='0.0.0.0', port=8000, debug=True)