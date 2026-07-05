import os

os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')

import yt_dlp
import vlc
import time
import random

class SpotifyClone:
    def __init__(self):
        self.is_active = False
        self.playlist = {
            #This is the playlist dictionary that you have to make as per your choice formar:- playlist_name: list of song names
        }
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.is_playing = False
        
        
    
        
    
    def play_from_search(self, query):
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'cookiefile': 'cookies.txt',
        }

        if query.startswith('http'):
            search_query = query
        
        else:
            search_query = f"ytsearch1:{query}"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
          
                info = ydl.extract_info(search_query, download=False)['entries'][0]
                audio_url = info['url']
                title = info.get('title', 'Unknown Track')

                media = self.instance.media_new(audio_url)
                self.player.set_media(media)
                self.player.play()
                self.is_playing = True
                
            except Exception as e:
                
                pass

    