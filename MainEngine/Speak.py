import pyttsx3

#Setting up voice for A.I.
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id) #We can change voices id to switch to different voice
engine.setProperty('rate', 160) #Increase voice rate for speech faster and decrease for slower
engine.setProperty('volume', 1.0)  #We can change volume here default volume is 1.0

#Speak function
def Say(text):
    """It takes string input and returns audio output"""
    print(f"A.I. : {text}\n")
    engine.say(text)
    engine.runAndWait()
