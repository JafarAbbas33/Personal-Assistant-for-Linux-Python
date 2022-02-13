import os
import youtube
import logging
import threading
import subprocess
import webbrowser

from commands_executor import shutdown
from Assistant import Assistant
from media_controller import stop_media, play_media, resume_media, pause_media

def log(data):
    logging.debug('\n\n\n' + data.encode('unicode-escape').decode('utf-8'))


def is_com_present(my_spoken_text, req = [], single = []):
    if all(x in my_spoken_text for x in req) or len(req) == 0:
        if len(single) == 0:
            for com in req:
                my_spoken_text = my_spoken_text.replace(com, '')
            my_spoken_text.strip()
            if my_spoken_text == '':
                return True
            return my_spoken_text
        if any(x in my_spoken_text for x in single):
            for com in single:
                my_spoken_text = my_spoken_text.replace(com, '')
            for com in req:
                my_spoken_text = my_spoken_text.replace(com, '')
            my_spoken_text = my_spoken_text.strip()
            if my_spoken_text == '':
                return True
            return my_spoken_text
    return False


def command_present(my_spoken_text):
    my_spoken_text = my_spoken_text.lower()

    if 'shutdown' in my_spoken_text:
        Assistant.terminate()
        shutdown()
        return True

    command_test = is_com_present(my_spoken_text, ['search', 'on google'], [])
    if command_test:
        Assistant.logger.info(command_test)
        url = 'https://www.google.com/search?channel=fs&client=ubuntu&q=' + command_test.replace(' ', '+')
        webbrowser.open(url, 2)
        return True

    if is_com_present(my_spoken_text, ['play', 'movie'], []):
        # Need implementation
        return False

    if 'type for me' in my_spoken_text:
        # Need implementation
        return False

    if is_com_present(my_spoken_text, [], ['play a random song', 'play a song', 'play some music', 'play some song', 'play music']):
        play_media('my_utils/assistant_replies/Sure sir! Playing songs!.wav', threaded = False)
        play_media(os.environ['music_directory'])
        return True

    command_test = is_com_present(my_spoken_text, ['play', 'youtube'], [])
    if command_test:
        Assistant.logger.info(command_test)
        youtube.download_and_play_song(command_test)
        return True

    if 'pause' in my_spoken_text:
        pause_media()
        return True

    if 'resume' in my_spoken_text:
        resume_media()
        return True

    if 'stop' in my_spoken_text:
        stop_media()
        return True
    
    if is_com_present(my_spoken_text, [], ['goodbye', 'quit', 'exit', 'good bye']):
        Assistant.logger.info('Heard exit command')
        # Assistant.terminate()
        Assistant.terminate_flag = True
        Assistant.logger.info('Returning after hearing exit command')
        return True
    
    return False
