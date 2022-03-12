import os
import sys
import time
import threading

from playsound import playsound

class Gui:
    assistant_window_canvas = None
    icon = None
    black_canvas = None
    root = None
    update_text = None
    bring_to_front = None
    minimize = None
    monitor = None
    screenshot = None
    mic = None
    mic_size = None
    mic_location = None

class Assistant:
    Gui = Gui
    assistant = None
    assistant_thread = None
    logger = None
    stop_playback = False
    terminate_flag = False

    @staticmethod
    def play_voice(string):
        if Assistant.Gui.root.state() == 'iconic':
            Gui.bring_to_front()

        Gui.update_text(string)
        Assistant.Gui.root.update()
        path = 'my_utils/assistant_replies/' + string + '.wav'
        if os.path.exists(path):
            playsound(path)
        Gui.minimize()
    
    @staticmethod
    def terminate(event):
        print()
        while threading.active_count() != 1:
            print('Waiting for other threads to quit...')
            time.sleep(0.3)
            
        Assistant.play_voice('Sayonara!')
        print('Gracefully exiting.')
        Assistant.logger.info('Gracefully exiting.')
        Assistant.Gui.root.destroy()
