# Light-Assistant V - 2.5 Alpha

# Note: Please Read the commands_hint.txt for learning the format of commands

Light is a local desktop voice assistant built in python, Instead of relying on start menu to open apps Light uses apps paths stored in registry and os module to open the apps
# Key Features
1. Advanced OS Integration (Uses Windows Registry 'winreg' to track paths and 'os.startfile' to open apps without using start menu)
2. Natural Voice Engine (By edge tts 'hi-IN-SwaraNeural')
3. Zero System Overheat (Built for handling low end devices)

# Initial Changes (Mandatory setup)
Before Running the 'main.py' file make sure you have changes all the paths in all files as per your pc paths
Open the following files and do the following changes
1. **alias_names.py** : Update the number dictionary in Number class as per the numbers you want to send whatsapp messages frequently. It should be in format **name:number**. In **Alias_names** class change the name as per your pronounciation.
2. **media.py** : Make sure you have **VLC** installed and change the **vlc path** in the **2nd line** as per your path.
3.  **registry.py** : You have to make some registry to run it perfectly. How to make it? It is given in 'registry_making.txt'.
