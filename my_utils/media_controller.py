from AssistantCommunicationsHandler import AssistantCommunicationsHandler
import os
from threading import Thread

def play_media(path):
    path = '"' + path + '"'
    print('Playing media...')
    Thread(target=lambda: os.system(' '.join(['audacious', '-H', '-q', path]))).start()

def stop_media():
    Thread(target=lambda: os.system(' '.join(['audacious', '-s']))).start()

def pause_media():
    Thread(target=lambda: os.system(' '.join(['audacious', '-H', '--pause']))).start()

def resume_media():
    Thread(target=lambda: os.system(' '.join(['audacious', '-H', '--play']))).start()
