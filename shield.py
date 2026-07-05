import tkinter as tk
import time

class Shield:

    def __init__(self):
        self.is_running = True

    def shielding(self):
        root = tk.Tk()
        root.withdraw()


        while self.is_running:
            try:
                clip = root.clipboard_get()
                if 'Sir' in clip or 'smart_pause' in clip:
                    root.clipboard_clear()
                    root.clipboard_append('Access Denied from Light AI. Message from Sarthak Sir, Nice Try But You Cant Copy Anything')
                    root.update()
            except:
                pass
            time.sleep(1)