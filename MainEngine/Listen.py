import speech_recognition as sr #pip install speechrecognition
from googletrans import Translator

def Listen(timer=None,threshold=300):

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = threshold
        if timer!=None:
            audio = r.listen(source,0,timer)
        else:
            audio = r.listen(source)
        
    try:
        print("Recognizing..")
        query = r.recognize_google(audio,language="hi")
        # print(f"You Said : {query}.")

    except:
        return ""

    query = str(query).lower()
    return TransaltionHnToEng(query)

#Translation Hindi to English
def TransaltionHnToEng(text):
    line = str(text)
    translate = Translator()
    result = translate.translate(line)
    data = result.text
    print(f"You: {data}.")
    return data.lower()

