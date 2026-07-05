
import time
import os
import webbrowser
import speech_recognition as sr
from alias_names import Alias_names, Number
from registry import Registry
from media import SpotifyClone
from yt_video import YT_Player
from clipboard import Clipboard
from shield import Shield
import pygame
import uuid
import asyncio
import edge_tts
import pygetwindow as gw
import pywhatkit
import threading


names = Alias_names()
register = Registry()
num = Number()
music = SpotifyClone()
clip = Clipboard()
yt = YT_Player()
shield = Shield()

class Light_AI_V_2_Alpha:
    
    def __init__(self):
        print('If you dont know commands of Light then please refer commands_hint.txt file')
        self.recognizer = sr.Recognizer()
        pygame.mixer.init()
        self.say('Sir, Aapka swagat hai. Mai system on kar rahi hu')
        self.running = True
        self.music_active = False
        self.yt_active = False
        self.new_volume = register.ai_volume
        self.exit = ['exit', 'quit', 'stop']
        self.pause_words = ['pause', 'off', 'halt', 'break']

        shield_thread = threading.Thread(target=shield.shielding)
        shield_thread.start()

    def smart_pause(self,active_music_thread, active_yt_thread,  music_thread = False):
        self.say('Sir, Mai 90 seconds ke liye pause le rahi hu.')
        active_thread = active_music_thread or active_yt_thread

        for second in range(90):

            if music_thread or not active_thread:
                break

            if not self.running:
                return
            
            time.sleep(1)
    
    def check(self, window):
        opened_windows = [w for w in gw.getAllWindows() if f'{window}' in w.title.lower()]
        if opened_windows:
            windows = opened_windows[0]
            if windows.isMinimized:
                windows.restore()
            windows.activate()
            return True
        return False
    
    async def speak(self, text_to_say):
        volume_offset = register.ai_volume - 100
        volume_parameter_string = f"{volume_offset:+}%"
        

        communicate = edge_tts.Communicate(
            text=text_to_say,
            voice="hi-IN-SwaraNeural",
            rate="+10%",
            pitch="+2Hz",
            volume=volume_parameter_string
        )
        
        temp_filename = f"light_audio_{uuid.uuid4().hex[:6]}.mp3"
        await communicate.save(temp_filename)
        
        pygame.mixer.music.load(temp_filename)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
            
        pygame.mixer.music.unload()
        try:
            os.remove(temp_filename)
        except OSError:
            pass

        
    def say(self, text):
        asyncio.run(self.speak(text))

    def run(self):
        try:
            while(self.running):
                with sr.Microphone() as source:
                    

                    try:
                        self.say('Sir, Aapka command boliye ')
                        self.recognizer.adjust_for_ambient_noise(source=source)

                        audio = self.recognizer.listen(source, 15, 8)
                        command = self.recognizer.recognize_google(audio)
                    except sr.UnknownValueError:
                        self.say('Sir, Mai aapki awaz ko sun nahi pai')
                        continue
                    except sr.RequestError:
                        self.say('Sir, Mai aapki awaz ko samajh nahi pai')
                        continue
                    except sr.WaitTimeoutError:
                        self.say('Sir, Aapke bolne ka samay khatam ho gaya hai')
                        continue
                    except:
                        continue
                
                print(command)
                command = command.lower()
                words = command.split()

                if words[0] == 'light':

                    if len(words) > 1:

                        if len(words) >= 4 and words[1] == 'who' and words[2] == 'are' and words[3] == 'you':
                            self.say(f'Sir, Mai {register.ai_name} version {register.ai_version} hu. Mujhe Sarthak Sir ne banaya hai joh T-C-E-T ke Student hai')

                        elif words[1] == 'open':

                            if len(words) >= 3:

                                if words[2] == 'youtube':

                                    if not self.check('chrome'):
                                        os.startfile(register.apps_paths['chrome'])
                                    time.sleep(1)
                                    webbrowser.open('https://www.youtube.com/')
                                    self.say('Sir, Maine Youtube open kar diya hai')

                                elif words[2] == 'whatsapp':

                                    if not self.check('chrome'):
                                        os.startfile(register.apps_paths['chrome'])
                                    time.sleep(1)
                                    webbrowser.open('https://web.whatsapp.com/')
                                    self.say('Sir, Maine Whatsapp open kar diya hai')

                                else:

                                    try:

                                        if not self.check(words[2]):
                                            os.startfile(register.apps_paths[names.alias_names[words[2]]])
                                        self.say(f'Sir, Maine {words[2]} open kar diya hai')
                                    except Exception as e:
                                        continue
                            
                            else:
                                self.say('Sir, Maine half command suna hai. Aap command wapas boliye.')

                        elif words[1] == 'message':

                            if len(words) > 3:

                                if not self.check('chrome'):
                                    os.startfile(register.apps_paths['chrome'])

                                message_words = command.split(' ', 3)
                                message_name = message_words[2]
                                message_sentence = message_words[3]

                                if message_name in num.number:
                                    self.say('Sir, Mai aapka message send kar rahi hu tab tak aap wait kijiye')
                                    number = f'+91{num.number[message_name]}'
                                    whatsapp_thread = threading.Thread(
                                        target=pywhatkit.sendwhatmsg_instantly,
                                        kwargs={'phone_no': number, 'message': message_sentence}
                                    )
                                    whatsapp_thread.start()

                                else:
                                    self.say('Sir, Aap jisko message bhejna chahte hai woh number register me nahi hai')
                            
                            else:
                                self.say('Sir, Maine half command suna hai. Aap command wapas boliye')

                        
                        elif words[1] == 'play':
                                
                            if len(words) > 2:
                                    
                                if len(words) >= 5 and words[2] == 'from' and words[3] == 'the' and words[4] == 'link':
                                    clipboard_string = clip.get_clipboard()
                                    if clipboard_string.startswith('https'):
                                        try:
                                            register.ai_volume = 60
                                            self.active_yt_thread = threading.Thread(
                                                target=yt.play_video, 
                                                args=[clipboard_string]
                                                )
                                            self.active_yt_thread.start()
                                            self.yt_active = True
                                            self.say('Sir, Mai video background me play kar rahi hu')
                                        except:
                                            pass
                                    else:
                                        self.say('Sir, Clipboard me kuch nahi hai')


                                elif not words[2] == 'from':
                                        music_word = command.split(' ', 2)

                                        try:
                                            register.ai_volume = 60
                                            self.active_music_thread = threading.Thread(
                                                target=music.play_from_search, 
                                                args=[music_word[2]]
                                                )
                                            self.active_music_thread.start()
                                            self.music_active = True
                                            self.say('Sir, Mai music play kar rahi hu background me')
                                        
                                        except Exception as e:
                                            pass    
                            
                            else:
                                self.say('Sir, Maine half command suna hai. Aap command wapas boliye')
                        
                        elif words[1] in self.pause_words:
                            self.smart_pause(active_music_thread=self.music_active, active_yt_thread=self.yt_active)

                            self.say('Sir, System active ho gaya hai wapas.')


                        
                        
                        
                        elif words[1] == 'search':

                            if len(words) >= 6 and words[3] == 'youtube':
                                search_sentence = command.split(' ', 5)[5]

                                if self.check('chrome'):
                                    webbrowser.open(f'https://www.youtube.com/results?search_query={search_sentence}')

                                else:
                                    os.startfile(register.apps_paths['chrome'])
                                    time.sleep(1)
                                    webbrowser.open(f'https://www.youtube.com/results?search_query={search_sentence}')
                                
                            elif len(words) >= 4:
                                search_sentence = command.split(' ', 3)[3]

                                if self.check('chrome'):
                                    webbrowser.open(f'https://www.google.com/search?q={search_sentence}')

                                else:
                                    os.startfile(register.apps_paths['chrome'])
                                    time.sleep(1)
                                    webbrowser.open(f'https://www.google.com/search?q={search_sentence}')

                        elif words[1] == 'increase' and words[2] == 'volume':
                            self.new_volume += 20
                            register.ai_volume = min(100, self.new_volume)
                            print(register.ai_volume)

                        elif words[1] == 'decrease' and words[2] == 'volume':
                            self.new_volume -= 20
                            register.ai_volume = max(30, self.new_volume)
                            print(register.ai_volume)
                        
                        elif words[1] in self.exit:

                            if len(words) >= 3 and self.music_active:
                                if words[2] == 'music':
                                    music.player.stop()
                                    self.music_active = False

                                elif words[2] == 'video' and self.yt_active:
                                    yt.player.stop()
                                    self.yt_active = False

                            else:
                                self.running = False
                                self.say('Sir, Abhi ke liye bye. Aapke next time System on karne ka wait karungi')
                                shield.is_running = False
                            
                        
                        else:
                            self.say('Sir, commannd abhi listed nahi hai.')
                    
                    else:
                        self.say('Sir, Aapne bas wake word bola hai')
                else:
                    self.say('Sir, Aapne galat wake word bola hai')
        except KeyboardInterrupt:
            self.say('Sir, Aapne Keyboard ne stop kar diya hai')
            shield.is_running = False

if __name__ == '__main__':

    ai = Light_AI_V_2_Alpha()
    ai.run()