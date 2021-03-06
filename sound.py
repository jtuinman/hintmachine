import configparser
import logging
import pygame
import atexit
import os
import sys
import time
import re
from sound_library import SoundLoggingHandler

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

class soundsystem():

    def clean():
        pygame.mixer.quit()

    sound_channel = None
    last_soundpath = ""
    def play_sound(soundpath):
        logger.info("Got request to play "+ soundpath)
        global sound_channel, last_soundpath
        try:
            ## Kill ALL current sounds except for music
            pygame.mixer.stop()
            if not os.path.exists(soundpath):
                logger.error(soundpath + " does not exist")
            if soundpath[-3:] != "ogg":
                logger.error("File requested was of type: " + soundpath[-3:] + " and might not work!")

            ## Calculate length first. This takes a few seconds on the pi.
            hint = pygame.mixer.Sound(soundpath)
            hint.set_volume(float(soundsystem.sound_volume) / 100)
            length = hint.get_length()
            logger.info("Length of sound bit is "+ str(int(length)) + " seconds.")
            hint.get_volume()

            ## Before playing, lower the volume of the music
            if pygame.mixer.music.get_busy():
                if(pygame.mixer.music.get_volume() > 0.1):
                    pygame.mixer.music.set_volume(0.1)
                    logger.info("Volume down to "+ str(int(pygame.mixer.music.get_volume())))
                else:
                    pygame.mixer.music.set_volume(0.0)
            last_soundpath = soundpath
            sound_channel = hint.play()
            logger.info("Playing "+ soundpath)
            if pygame.mixer.music.get_busy():
                time.sleep(length +1)
                pygame.mixer.music.set_volume(float(soundsystem.music_volume) / 100)

        except Exception as e:
            logger.error("Tried to play sound file but got error: " + str(e))
        logger.info("Done with " + soundpath)

    ## Background music, changes for each scene
    ## Note that the fade blocks the state_machine from ansering requests, so in theory if players are fast they
    ## will need to pull triggers multiple times
    music = None
    def play_music(soundpath):
        soundsystem.stop_music()
        global music
        pygame.mixer.music.load(soundpath)
        music = soundpath
        pygame.mixer.music.set_volume(float(soundsystem.music_volume) / 100)
        pygame.mixer.music.play(-1)
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def stop_music():
        fade = soundsystem.config.getint("Escape","fadeout")
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

##If play_music is called first, the hint will play after.
##If play_sound is called first, two are played together (as I would like.)
#soundsystem.play_sound(soundsystem.sounddir + soundsystem.config.get("Escape","music_state_state1"))
#soundsystem.play_music(soundsystem.sounddir + soundsystem.config.get("Escape","music_state_state2"))
