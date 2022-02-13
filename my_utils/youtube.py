from media_controller import stop_media, play_media, resume_media, pause_media
from Assistant import Assistant
from youtubesearchpython import SearchVideos
from pytube import YouTube

import os
import json
import urllib
import threading


def get_video_url(query):
    Assistant.logger.info('Getting video URL')
    search = SearchVideos(query, offset = 1, mode = "json", max_results = 3)
    result = json.loads(search.result())
    vid_id = result['search_result'][0]['id']
    return 'http://youtube.com/watch?v=' + vid_id

def download_video(query):
    vid_url = get_video_url(query)
    yt = YouTube(vid_url)
    selected_file = yt.streams.filter(adaptive=True, only_audio=True)[0]
    Assistant.logger.info('Downloading...')
    selected_file.download()
    return selected_file.default_filename

def _download_and_play_song(query):
    c = 0
    while c < 6:
        try:
            vid_name = download_video(query)
            play_media(vid_name)
            break
        except urllib.error.HTTPError:
            print('Failed! Retrying...')
            c += 1
    
def download_and_play_song(query):
    threading.Thread(target = lambda: _download_and_play_song(query)).start()

if __name__ == '__main__':
    download_and_play_song('arora')

