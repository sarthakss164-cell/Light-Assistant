import tkinter as tk

class Clipboard:

        
    def get_clipboard(self):

        root = tk.Tk()

        root.withdraw()

        try:
            text = root.clipboard_get()

            return text
        except tk.TclError:
            return ''
        
