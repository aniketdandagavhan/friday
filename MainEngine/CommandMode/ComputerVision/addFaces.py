from MainEngine.Listen import Listen
from MainEngine.Speak import Say
from MainEngine.Vision.FaceRecognition import Model_trainer,Sample_generator

def addFace():
    Say("What should I call you?")
    name = Listen()
    name = name.replace("call","").replace("me","").replace("him","").replace(" ","").replace("  ","")
    Say(f"Okay {name}, Saving Face in database! Please stay in front of camera!")
    Sample_generator.sample_generator(faceName=name)
    Model_trainer.model_trainer()
    Say("Done Sir.")