
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

# -----------------------------------------------------------------------

sys.path.insert(0, 'utils')
sys.path.insert(0, 'my_utils')
full_text = ''

import tkinter as tk
from PIL import Image
from PIL import ImageTk
from icecream import ic, install
from PIL import ImageFont, ImageDraw

from AssistantCoreInitializer import AssistantCoreInitializer
from AssistantCommunicationsHandler import AssistantCommunicationsHandler

install()

#--------------------------------------------------------------
# Handling GUI
#--------------------------------------------------------------

class TextUtil:
    pass
 
def update_text(text):
    canvas.itemconfigure(text_label, text=text)
    return


def bring_to_front():
    update_text("")
    global image, mic, w, h, im, oo, monitor
    with mss.mss() as sct:
        sct_img = sct.grab(monitor)
        #sct_img = sct.shot(output = "xoxo" + x + ".jpg")
        im = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        #AssistantCommunicationsHandler.screenshot = im.copy()
        
    im = Image.blend(im,image,0.65)
    width, height = image.size
    past_w = round((width-w)/2)
    past_h = round((height-h)/2)
    im.paste(mic, (past_w, past_h), mic)
    oo = ImageTk.PhotoImage(im)
    root.state('normal')
    
    canvas.itemconfigure(image_label, image=oo)
    
    TextUtil.im = im
    TextUtil.current_h = past_h + 250


def minimize():
    while root.state() == 'normal':
        root.state('iconic')
        root.update()
        time.sleep(0.5)

def keep_screen_awake():
    os.system('xdg-screensaver reset')
    AssistantCommunicationsHandler.logger.info('Pinged!')
    root.after(150000, keep_screen_awake)

def key_pressed(event):
    if '' == event.char:
        AssistantCommunicationsHandler.stop_playback = True
    elif '' == event.char:
        AssistantCommunicationsHandler.logger.info('Request destroy')
        AssistantCommunicationsHandler.terminate()

def on_closing():
    AssistantCommunicationsHandler.logger.info('Destroying')
    AssistantCommunicationsHandler.terminate()


# -------------------------------------------------------------


def get_logger():
    logger = logging.getLogger('Natalie')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('Natalie.log')
    #f_format = logging.Formatter('%(asctime)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(filename)s - %(lineno)d - %(message)s')
    handler.setFormatter(f_format)
    logger.addHandler(handler)    
    logger.propagate = False
    return logger

def set_cwd():
    if '/' not in sys.argv[0]:
        return
    script_location = sys.argv[0].split('/')
    script_location.pop(-1)
    cwd = '/'.join(script_location)
    os.chdir(cwd)

if __name__ == '__main__':
    set_cwd()
    
    root = tk.Tk()

    icon = ImageTk.PhotoImage(master=root, file='utils/favicon.ico')
    root.wm_iconphoto(True, icon)

    root.title("Assistant")
    root.attributes("-fullscreen", True)

    mic = Image.open("utils/Google_mic.png")
    mic = mic.resize((58, 80), Image.ANTIALIAS)
    w,h=mic.size
    ww = root.winfo_screenwidth()
    hh = root.winfo_screenheight()    
    monitor = {'left': 0, 'top': 0, 'width': ww, 'height': hh}
    # font = ImageFont.truetype("utils/Montserrat-Medium.ttf", size=70)
    # font = ImageFont.load_default()
    spacing_bw_text = 10
    o_w = 0

    # Fill up AssistantCommunicationsHandler
    AssistantCommunicationsHandler.root = root
    AssistantCommunicationsHandler.minimize = minimize
    AssistantCommunicationsHandler.logger = get_logger()
    AssistantCommunicationsHandler.update_text = update_text
    AssistantCommunicationsHandler.bring_to_front = bring_to_front

    image = Image.new("RGB", (ww, hh), "black")
    oo = ImageTk.PhotoImage(image)

    canvas = tk.Canvas(root, width=ww, height=hh)
    canvas.pack()
    image_label = canvas.create_image(ww, 0, image=oo, anchor="ne")
    text_label = canvas.create_text(ww//2, hh/2+200, text="", font=("Ubuntu", 26), fill="white")

    bring_to_front()
    update_text("Initializing")
    AssistantCommunicationsHandler.logger.info('-----------------------------------------\n')
    AssistantCommunicationsHandler.logger.info('Initializing')

    threading.Thread(target = AssistantCoreInitializer).start()

    # Uncomment if you have xdg-screensaver installed and is funtioning
    # root.after(150000, keep_screen_awake)
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.bind('<Key>',key_pressed)

    root.mainloop()



