import paho.mqtt.client as mqtt
import time
import signal
import sys


def signal_handler(sig, frame):
    client.loop_stop()
    print("Exiting")
    sys.exit(0)

def on_connect(client, userdata, flags, rc):
    print("connected with resultcode " + str(rc))
    client.subscribe("SOUNDMACHINE/+") 

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))
    if message.topic == "SOUNDMACHINE/HINTS":
        with open('home/pi/mqtt_update.txt', 'a+') as f:
            f.write("received topic2")

signal.signal(signal.SIGINT, signal_handler)

broker_address = "192.168.178.30"  # Broker address
port = 1883  # Broker port
# user = "yourUser"                    #Connection username
# password = "yourPassword"            #Connection password

client = mqtt.Client()  # create new instance
# client.username_pw_set(user, password=password)    #set username and password
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback

client.connect(broker_address, port=port)  # connect to broker

client.loop_forever()

