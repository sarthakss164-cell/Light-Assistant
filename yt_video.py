import yt_dlp
import vlc
import time

class YT_Player:
    def __init__(self):

        self.ydl_opts = {
            'format':'bestvideo[height<=1080]+bestaudio/best',# best for the quality to be 1080p or 720p
            'quiet': True,# no background noice 
            'noplaylist': True,# if 1st thing is playlist then ignore it
            'cookiefile': 'cookies.txt',
        }
        self.instance = vlc.Instance('--no-xlib', '--quiet', '--video-on-top') # Window for player
        self.player = self.instance.media_player_new() # Make new window and new object

    def play_video(self, user_input):
        if user_input.startswith("http"): # If input start with http then direct go to address
            search_query = user_input
        else:

            search_query = f"ytsearch1:{user_input}"# else go for search in youtube

        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(search_query, download=False) # Gives all the html info and makes the download false
                video_data = info['entries'][0] if 'entries' in info else info # Takes the 1st video from search
                
                self.start_vlc(video_data)

        except Exception as e:
            pass

    def start_vlc(self, video_data):

        formats = video_data.get('requested_formats') # Used as for 1080p audio file is different and video file is different
        
        if formats and len(formats) >= 2: # if we get 2 formats means audio and video files 
            v_url = formats[0]['url'] # The HD Video link
            a_url = formats[1]['url'] # The HD Audio link
            
            media = self.instance.media_new(v_url)
            self.player.set_media(media)
            self.player.play()
            
            
            self.player.add_slave(vlc.MediaSlaveType.audio, a_url, True)
        else:
            
            media = self.instance.media_new(video_data['url'])
            self.player.set_media(media)
            self.player.play()

       

        try:
            while True:
                time.sleep(0.1)
                

                if self.player.get_state() in [vlc.State.Ended, vlc.State.Stopped]:
                    break
        except KeyboardInterrupt:
            
            pass
        finally:
            self.player.stop()

