from pydoc import splitdoc
import random
import json
import webbrowser
import pyautogui
import torch
import time
from MainEngine.Listen import Listen
from MainEngine.Speak import Say
from MainEngine.Brain import NeuralNet
from MainEngine.NeuralNetwork import bag_of_words, tokenize
from MainEngine.UserAuthProtocol import userAuth
from MainEngine.Hotword import hotword
from MainEngine.CommandMode.ComputerVision import addFaces, recogniseFaces
from MainEngine.Vision.HandDetectionModule.virtualMouse import virtualMouse
from MainEngine.BigBrain.openairunner import bigBrain
from MainEngine.CommandMode.TimeRelated.setTimer import setTimer, setSnooze
from MainEngine.utils.saveJson import saveJson, saveRem, readRem
from MainEngine.TaskExecution.openCloseTask import openTaskExec, closeTaskExec
from MainEngine.clap import Tester
import os
import threading

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open('.\MainEngine\intents.json', 'r') as file:
    intents = json.load(file)

FILE = ".\MainEngine\Database\TrainedData\TrainDAta.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size,hidden_size,output_size).to(device=device)
model.load_state_dict(model_state)
model.eval()

#A.I. Coding starts from here
Name = "Friday"
Admin = "Boss"

def Main(sentence):
    '''main function, should be responsible to manage each and every task and feature of ai and also other third party features'''

    #Base AI model.
    query = sentence
    sentence = tokenize(sentence)
    x = bag_of_words(sentence,all_words)
    x = x.reshape(1,x.shape[0])
    x = torch.from_numpy(x).to(device)
    output = model(x)
    _, predicted = torch.max(output,dim=1)

    tag = tags[predicted.item()]
    probabilities = torch.softmax(output,dim=1)
    prob = probabilities[0][predicted.item()]
    if prob.item() > 0.90:
        for intent in intents['intents']:
            if tag == intent['tag']:
                reply = random.choice(intent['responses'])
                Say(reply) #self coded data reply

                if tag=="addFace":
                    addFaces.addFace()
                
                elif tag=="recogniseFaces":
                    recogniseFaces.recogniseFaces()
                
                elif tag=="bye":
                    return True
                
                elif tag=="virtualMouse":
                    virtualMouse()
                
                elif tag=="gmap":
                    try:
                        spliterList = ["find", "of", "to", "for"]
                        splitter = False
                        for i in spliterList:
                            if i in query:
                                splitter = i
                                search = "+".join(query.split(splitter)[1].split(" "))
                                break
                        if not splitter:
                            Say("Where you want to go?")
                            search = Listen()
                            search = "+".join(search.split(" "))
                        webbrowser.open(f"https://www.google.com/maps/search/{search}")
                        # Say("Should I open directions for the same?")
                        # query = Listen()
                        # if "yes" in query.lower() or "yeah" in query.lower() or "go ahead" in query.lower() or "ok" in query.lower():
                        time.sleep(2)
                        pyautogui.click(71,600)
                        pyautogui.click(71,650)

                    except Exception as e:
                        Say("something went wrong! Error logged.")
                        saveJson(e)

                elif tag=="remember":
                    try:
                        spliterList = ["this", "that", "it"]
                        splitter = False
                        for i in spliterList:
                            if i in query:
                                splitter = i
                                reminder = query.split(splitter)[1]
                                if reminder is None or reminder in [""," "]:
                                    splitter = False
                                break
                        if not splitter:
                            Say("What should I remember?")
                            reminder = Listen()
                        saveRem(reminder)
                        Say("done!!")

                    except Exception as e:
                        Say("something went wrong! Error logged.")
                        saveJson(e)

                elif tag=="readReminder":
                    try:
                        filterList = ["today", "yesterday", "tomorrow"]
                        filter = False
                        for i in filterList:
                            if i in query:
                                filter = i
                                break
                        if not filter:
                            filter = "today"
                        Say(f"{filter}'s notes are")
                        Say(readRem(filter))

                    except Exception as e:
                        Say("something went wrong! Error logged.")
                        saveJson(e)
                
                elif tag=="open":
                    openTaskExec(query)

    #openAi integration for more complex and advance AI model
    elif query!="":
        res = bigBrain(query)
        Say(res)
        
if not userAuth():
    Say("Friday is turning off...")
    exit()

isRunning = True

#Hotword Loop
while True:
    Say("Listening boss!!")
    chat_log_template = f"\n{Admin}: who are you?\n{Name}: I am an {Name} created by {Admin}. How can I help you today?"
    #Main Function Loop
    while True:
        if isRunning:
            query = Listen()
            try:
                if "multiple commands" in query:
                    Say("Prepared for multiple commands, Boss!!")
                    sentences = Listen()
                    for sentence in sentences:
                        r = Main(sentence)
                    if r:
                        isRunning = False
                    else:
                        continue

                else:
                    r = Main(query)
                    if r:
                        isRunning = False
                    else:
                        continue
                
            except Exception as e:
                Say("something went wrong! Error logged.")
                saveJson(e)
            
        if Tester():
            isHotword = True

        
        

                


    