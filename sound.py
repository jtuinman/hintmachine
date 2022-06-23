import configparser
import pygame
import atexit
import os
import sys

def clean():
    pygame.mixer.quit()
  

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
    #logger.info("Now initalizing mixer")
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()  

## When CTRL-Cing python script, make sure that the mixer and pins are released
atexit.register(clean)



sounddir = config.get("Escape", "sounddir") + "/"
music_volume = config.getfloat("Escape", "music_volume")
sound_volume = config.getfloat("Escape", "sound_volume")
pygame.mixer.music.set_volume(music_volume / 100)