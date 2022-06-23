import configparser
import pygame
import atexit
import os
import sys
import time
import re

def clean():
    pygame.mixer.quit()
  
## Background music, changes for each scene
## Note that the fade blocks the state_machine from ansering requests, so in theory if players are fast they
## will need to pull triggers multiple times
music = None
def play_music(soundpath):
    stop_music()
    global music
    pygame.mixer.music.load(soundpath)
    music = soundpath
    pygame.mixer.music.set_volume(float(music_volume) / 100)
    pygame.mixer.music.play(-1)
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

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

## When CTRL-Cing python script, make sure that the mixer and pins are released
atexit.register(clean)

sounddir = config.get("Escape", "sounddir") + "/"
music_volume = config.getfloat("Escape", "music_volume")
sound_volume = config.getfloat("Escape", "sound_volume")
pygame.mixer.music.set_volume(music_volume / 100)

play_music(sounddir + config.get("Escape","music_state_state1"))
