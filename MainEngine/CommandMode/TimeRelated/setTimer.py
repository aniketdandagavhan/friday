import time
import threading
from playsound import playsound

snooze = True
soundPath = r".\\MainEngine\Database\AlarmSounds\\aot.mp3"

def setSnooze(bool):
    snooze = bool

def playSoundThread():
    playsound(soundPath)

def setTimer(query='minutes', num=10):
    sleepTime = num if query=='seconds' else num*60
    time.sleep(sleepTime)
    print("playing song")
    t = threading.Thread(target=playSoundThread)
    t.start()
    
    
