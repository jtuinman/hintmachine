import paho.mqtt.client as mqtt
import time
import signal
import sys

def signal_handler(sig, frame):
    clientSubscribe.loop_stop()
    print("Exiting")
    sys.exit(0)

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))


signal.signal(signal.SIGINT, signal_handler)
clientSubscribe = mqtt.Client("Mixer")
clientSubscribe.connect("localhost") 

clientSubscribe.loop_start()
clientSubscribe.unsubscribe("#")
clientSubscribe.subscribe("SOUNDMACHINE/+")

clientSubscribe.on_message = on_message 
 
time.sleep(60)
clientSubscribe.loop_stop()