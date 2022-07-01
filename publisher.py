import paho.mqtt.client as mqtt
import time
import signal
import sys
import json

def signal_handler(sig, frame):
    clientPublish.loop_stop()
    print("Exiting")
    sys.exit(0)

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))


signal.signal(signal.SIGINT, signal_handler)

clientPublish = mqtt.Client("TestPublish")
clientPublish.connect("192.168.178.30")


test = "lol"
musicName = "music_state_state1"
message = {
        "command": musicName
        }

jsonDump = json.dumps(message)
topic="SOUNDMACHINE/HINTS"
clientPublish.publish(topic, jsonDump)
print(jsonDump)

time.sleep(1)

#test = "Ha!"
#soundName = "music_state_state1"
#message = {
#        "command": soundName
#        }

#jsonDump = json.dumps(message)
#topic="SOUNDMACHINE/HINTS"
#clientPublish.publish(topic, jsonDump)
#print(jsonDump)

clientPublish.loop_stop()