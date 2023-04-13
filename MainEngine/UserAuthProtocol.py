from MainEngine.Speak import Say
from MainEngine.Vision.FaceRecognition.Face_recognition import face_recognizer

def userAuth():
    Say("initiating user auth protocol")
    lock = face_recognizer(useCat="lock",userCount=1,enableShow=False)
    print(lock)
    if not lock[1]:
        Say(f"{lock[0][-1]} you are not authorized")
        return(False)
    return(True)