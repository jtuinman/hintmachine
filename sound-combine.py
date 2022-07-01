import configparser
import logging
import pygame
import atexit
import os
import sys
import time
import re
from sound_library import SoundLoggingHandler
import paho.mqtt.client as mqtt
import signal

import json

## Prereqs: python 3
##sudo apt install git
##sudo apt install pip
##python3 -m pip install -U pygame --user
##sudo apt-get install git curl libsdl2-mixer-2.0-0 libsdl2-image-2.0-0 libsdl2-2.0-0
##sudo bash -c 'echo -e " defaults.pcm.card 1 \ndefaults.ctl.card 1" > /etc/asound.conf'

## Logger setup
logger = logging.getLogger(__name__)
logging.getLogger('werkzeug').setLevel(logging.ERROR)
entriesHandler = SoundLoggingHandler()
logger.addHandler(logging.StreamHandler())
logger.addHandler(entriesHandler)
logger.setLevel(logging.INFO)


def clean():
    pygame.mixer.quit()

sound_channel = None
last_soundpath = ""
def play_sound(soundpath):
    hint = pygame.mixer.Sound(soundpath)
    length = hint.get_length()
    hint.set_volume(float(sound_volume) / 100)
    logger.info("get_busy : " + str(pygame.mixer.music.get_busy()))
    if pygame.mixer.music.get_busy():
                if(pygame.mixer.music.get_volume() > 0.1):
                    pygame.mixer.music.set_volume(0.1)
                    logger.info("Volume down to "+ str(int(pygame.mixer.music.get_volume())))
                else:
                    pygame.mixer.music.set_volume(0.0)
    hint.play()
    if pygame.mixer.music.get_busy():
        time.sleep(length +1)
        pygame.mixer.music.set_volume(float(music_volume) / 100)

## Background music, changes for each scene
## Note that the fade blocks the state_machine from ansering requests, so in theory if players are fast they
## will need to pull triggers multiple times
music = None
def play_music(soundpath):
    stop_music()
    #global music
    #pygame.mixer.music.load(soundpath)
    #music = soundpath
    #pygame.mixer.music.set_volume(float(music_volume) / 100)
    #pygame.mixer.music.play(-1)
    #while pygame.mixer.music.get_busy():
    #pygame.time.Clock().tick(10)
    pygame.mixer.music.load(soundpath)
    pygame.mixer.music.play(-1)
    logger.info("get_busy : " + str(pygame.mixer.music.get_busy()))

def stop_music():
    fade = config.getint("Escape","fadeout")
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(fade * 1000)
        time.sleep(fade)
    global music
    music = None

def get_sounds_from_folder(dir):
    return sorted([f for f in os.listdir(dir) if re.search(r'.+\.(wav|ogg|mp3)$', f)])


## Init stuff from here
configfilename = "sound.conf"
configfile = (os.path.join(os.getcwd(), configfilename))
config = configparser.ConfigParser()
try:
    with open(configfile,'r') as configfilefp:
        config.read_file(configfilefp)
except:
    print("Could not read " + configfile)
    sys.exit()

if not pygame.mixer.get_init():
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()  

## When CTRL-Cing python script, make sure that the mixer is released
atexit.register(clean)

sounddir = config.get("Escape", "sounddir") + "/"
music_volume = config.getfloat("Escape", "music_volume")
sound_volume = config.getfloat("Escape", "sound_volume")
pygame.mixer.music.set_volume(music_volume / 100)

logger.info("Number of channels: " + str(pygame.mixer.get_num_channels()))

def signal_handler(sig, frame):
    client.loop_stop()
    print("Exiting")
    sys.exit(0)

def on_connect(client, userdata, flags, rc):
    print("connected with resultcode " + str(rc))
    client.subscribe("SOUNDMACHINE/+") 

def on_message(client, userdata, message):
    messageBody = str(message.payload.decode("utf-8"))
    print("received message: " , message)
    jsonObject = json.loads(messageBody)
    print(jsonObject["command"])
    if message.topic == "SOUNDMACHINE/HINTS":
        play_sound(sounddir + config.get("Escape",jsonObject["command"]))
    if message.topic == "SOUNDMACHINE/MUSIC":
        play_music(sounddir + config.get("Escape",jsonObject["command"]))

signal.signal(signal.SIGINT, signal_handler)

broker_address = "192.168.178.30"  # Broker address
#broker_address = "192.168.2.69"  # Broker address
port = 1883  # Broker port
# user = "yourUser"                    #Connection username
# password = "yourPassword"            #Connection password

client = mqtt.Client()  # create new instance
# client.username_pw_set(user, password=password)    #set username and password
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback

client.connect(broker_address, port=port)  # connect to broker

client.loop_forever()


