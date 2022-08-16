#!/usr/bin/env python3

import os
import mss
import sys
import time
import logging
import textwrap
import threading

# ---------------------------- PERSONAL EDIT ----------------------------

os.environ['assistant_credentials'] = 'YOUR ASSISTANT CREDENTIALS FILE LOCATION'
os.environ['assistant_device_id'] = 'YOUR ASSISTANT DEVICE ID'
os.environ['assistant_device_config'] = 'YOUR ASSISTANT DEVICE CONFIG FILE LOCATION'

os.environ['music_directory'] = 'YOUR MUSIC DIRECTORY'

os.environ['hotword_full_path'] = 'YOUR HOTWORD PPN FILE PATH' # My personal? - 'my_utils/natalie.ppn'
os.environ['hotword_library_path'] = 'YOUR HOTWORD LIBRARY FILE PATH' # Ends with '/libpv_porcupine.so'
os.environ['hotword_model_file_path'] = 'YOUR HOTWORD MODEL FILE PATH' # Ends with '/porcupine_params.pv'
os.environ['hotword_keyword_file_paths'] = 'YOUR HOTWORD KEYWORD FILE PATH' # Ends with '/keyword_files'

# Updating environment variables
if os.environ['music_directory'] == 'YOUR MUSIC DIRECTORY':
    from STAGING_FOLDER import environ
    environ.update_enviroment_variables()

# -----------------------------------------------------------------------

def fix_paths():
    sys.path.insert(0, 'utils')
    sys.path.insert(0, 'my_utils')

    # print(sys.argv[0])
    if '/' not in sys.argv[0]:
        return
    # print('Out')
    script_location = sys.argv[0].split('/')
    script_location.pop(-1)
    cwd = '/'.join(script_location)
    os.chdir(cwd)

fix_paths()

import tkinter as tk
from PIL import Image
from PIL import ImageTk
from icecream import ic, install
from PIL import ImageFont, ImageDraw

from AssistantCoreInitializer import AssistantCoreInitializer
from Assistant import Assistant

install()

#--------------------------------------------------------------
# Handling GUI
#--------------------------------------------------------------
 
def update_text(text):
    canvas.itemconfigure(text_label, text=text)
    return

def bring_to_front():
    # Assistant.Gui.root.update()
    # if root.state() == 'normal':
    #     return

    update_text("")

    mic = Assistant.Gui.mic
    black_canvas = Assistant.Gui.black_canvas

    with mss.mss() as sct:
        sct_img = sct.grab(Assistant.Gui.monitor)
        # sct_img = sct.shot(output = "xoxo" + x + ".jpg")
        screenshot = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        # Assistant.screenshot = screenshot.copy()
        
    Assistant.Gui.screenshot = screenshot

    assistant_window_canvas = Image.blend(screenshot, black_canvas, 0.65)
    assistant_window_canvas.paste(mic, (Assistant.Gui.mic_location['x'], Assistant.Gui.mic_location['y']), mic)
    assistant_window_canvas = ImageTk.PhotoImage(assistant_window_canvas)

    Assistant.Gui.assistant_window_canvas = assistant_window_canvas
    root.state('normal')
    
    canvas.itemconfigure(image_label, image=assistant_window_canvas)

def minimize():
    while root.state() == 'normal':
        root.state('iconic')
        root.update()
        time.sleep(0.5)

def keep_screen_awake():
    os.system('xdg-screensaver reset')
    Assistant.logger.info('Pinged!')
    root.after(150000, keep_screen_awake)

def key_pressed(event):
    if '' == event.char:
        Assistant.stop_playback = True
    elif '' == event.char:
        Assistant.logger.info('Request destroy')
        Assistant.stop_playback = True
        Assistant.terminate_flag = True
        # Assistant.terminate()


# -------------------------------------------------------------


def get_logger():
    logger = logging.getLogger('Natalie')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('Natalie.log')
    # terminal_logger = logging.StreamHandler(sys.stdout) # Uncomment to print logs to terminal as well  
    # f_format = logging.Formatter('%(asctime)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s')
    # f_format = logging.Formatter('%(asctime)s - %(filename)s - %(lineno)d - %(message)s')
    f_format = logging.Formatter('%(filename)s - %(lineno)d - %(message)s')
    handler.setFormatter(f_format)
    # terminal_logger.setFormatter(f_format) # Uncomment to print logs to terminal as well  
    logger.addHandler(handler)  
    # logger.addHandler(terminal_logger) # Uncomment to print logs to terminal as well  
    logger.propagate = False
    return logger


def initialize_root_window():
    root = tk.Tk()

    Assistant.Gui.icon = ImageTk.PhotoImage(master=root, file='utils/favicon.ico')
    root.wm_iconphoto(True, Assistant.Gui.icon)

    root.title("Assistant")
    root.attributes("-fullscreen", True)
    return root




if __name__ == '__main__':
    root = initialize_root_window()
    #print(dir(root)) # after # generate_event # destroy
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()    
    # font = ImageFont.truetype("utils/Montserrat-Medium.ttf", size=70)
    # font = ImageFont.load_default()

    # Fill up Assistant
    Assistant.Gui.monitor = {'left': 0, 'top': 0, 'width': screen_width, 'height': screen_height}
    Assistant.Gui.mic = Image.open("utils/Google_mic.png")
    Assistant.Gui.mic_size = {'width': 58, 'height': 80}
    Assistant.Gui.mic_location = {'x': round((screen_width-Assistant.Gui.mic_size['width'])/2), 'y': round((screen_height-Assistant.Gui.mic_size['height'])/2)}
    Assistant.Gui.root = root
    Assistant.Gui.minimize = minimize
    Assistant.Gui.update_text = update_text
    Assistant.Gui.bring_to_front = bring_to_front
    Assistant.Gui.black_canvas = Image.new("RGB", (screen_width, screen_height), "black")

    black_canvas = ImageTk.PhotoImage(Assistant.Gui.black_canvas)

    Assistant.logger = get_logger()

    canvas = tk.Canvas(root, width=screen_width, height=screen_height)
    canvas.pack()
    image_label = canvas.create_image(screen_width, 0, image=black_canvas, anchor="ne")
    text_label = canvas.create_text(screen_width//2, screen_height/2+200, text="", font=("Ubuntu", 26), fill="white")

    bring_to_front()
    update_text("Initializing")
    Assistant.logger.info('----------------------------------------------------------------------------------------------------------------------------------------------\n')
    Assistant.logger.info('Initializing')

    Assistant.assistant_thread = threading.Thread(target=AssistantCoreInitializer).start()

    # Uncomment if you have xdg-screensaver installed and is funtioning
    # root.after(150000, keep_screen_awake)
    
    root.bind("<<terminate>>", Assistant.terminate)
    root.bind('<Key>', key_pressed)

    root.mainloop()



