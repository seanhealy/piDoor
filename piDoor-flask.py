from flask import Flask, request
from twilio.rest import TwilioRestClient
from time import sleep

import pifacedigitalio
import json
import sys
import time

config = json.loads(open("config.json").read())
pifacedigital = pifacedigitalio.PiFaceDigital()

account_sid = config["twilio"]["account_sid"]
auth_token  = config["twilio"]["auth_token"]
client = TwilioRestClient(account_sid, auth_token)

def send_twilio_message(message):
    message = client.messages.create(body=message,
        to="+17808854376",    # Replace with your phone number
        from_="+15874007326") # Replace with your Twilio number
    print message.sid

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
        status = toggle_door(int(door_id))
    else:
        status = "Unknown Door: {0}".format(door_id)

    datetime = time.strftime("%Y-%m-%d %H:%M:%S")
    send_twilio_message("{0} at {1}".format(status, datetime))
    return status

if __name__ == "__main__":
    context = ('fullchain.pem', 'privkey.pem')
    app.run(host='0.0.0.0', port=2021, debug=True, ssl_context=context)
