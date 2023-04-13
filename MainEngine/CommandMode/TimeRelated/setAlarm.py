from datetime import datetime
from signal import alarm
from playsound import playsound

print(datetime.now().hour, datetime.now().day, datetime.now().minute, datetime.now().strftime("%I-%M-%p"))
def setAlarm(setDate=datetime.now().date(), setHour=0, setMinutes=0):
    alarmSoundPath = ""
    if datetime.now().date()==setDate and datetime.now().hour==setHour and datetime.now().minute==setMinutes:
        playsound(alarmSoundPath)

 #compare given time with current time and check that if given time is in range of remaining time if it is then just don't ask for am/pm and if not then ask for it.