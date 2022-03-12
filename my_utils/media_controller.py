import subprocess, time, os
from threading import Thread
from playsound import playsound
from Assistant import Assistant


queued_media_pid = None
def play_media(path, threaded=True):
    cmd = ['nohup', 'vlc', '"' + path + '"', '&']
    os.system(' '.join(cmd))
    return True


    subprocess.run(cmd)
    stop_media()
        
    print('Playing media...')
    c = subprocess.Popen(['cvlc', '--mmdevice-volume=0.9', '--random', '--no-video', '--play-and-exit', path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    
    global queued_media_pid
    queued_media_pid = str(c.pid)
    if not threaded:
        c.communicate()

        
def stop_media():
    if queued_media_pid != None:
        subprocess.Popen(['kill', '-s', 'SIGTERM', queued_media_pid],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).communicate()

def pause_media():
    if queued_media_pid != None:
        subprocess.Popen(['kill', '-s', 'SIGSTOP', queued_media_pid],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).communicate()
        
def resume_media():
    if queued_media_pid != None:
        subprocess.Popen(['kill', '-s', 'SIGCONT', queued_media_pid],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).communicate()


    
# For audacious
'''
def play_media(path, threaded = True):
    path = '"' + path + '"'
    print('Playing media...')
    if threaded:
        Thread(target=lambda: os.system(' '.join(['audacious', '-H', '-q', path]))).start()
    else:
        os.system(' '.join(['audacious', '-H', '-q', path]))
        
def stop_media():
    Thread(target=lambda: os.system(' '.join(['audacious', '-s']))).start()

def pause_media():
    Thread(target=lambda: os.system(' '.join(['audacious', '-H', '--pause']))).start()

def resume_media():
    Thread(target=lambda: os.system(' '.join(['audacious', '-H', '--play']))).start()
'''
