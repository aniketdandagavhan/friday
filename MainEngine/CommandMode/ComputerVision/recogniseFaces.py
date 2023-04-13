from MainEngine.Vision.FaceRecognition.Face_recognition import face_recognizer
from MainEngine.Speak import Say

def recogniseFaces():
    recognisedResponse = face_recognizer(useCat="faceRecognition",userCount=3,enableShow=True)
    Say(f"Hmmm! I can see {len(recognisedResponse[0])} of you")
    for name in recognisedResponse[0]:
        Say(f"Hii! {name} sir!")