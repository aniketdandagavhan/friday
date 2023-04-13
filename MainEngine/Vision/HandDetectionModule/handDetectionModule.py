import cv2
import mediapipe as mp
import time
import math

class handDetector():

    def __init__(self, mode=False, maxhands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxhands = maxhands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxhands, self.modelComplexity, self.detectionCon, self.trackCon)

        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4,8,12,16,20]
    
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(image=imgRGB)

        if self.results.multi_hand_landmarks:
            drawSpecsLm = self.mpDraw.DrawingSpec((0,0,255),2,1)
            drawSpecs = self.mpDraw.DrawingSpec((0,255,0),2,1)
            for handLandmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLandmarks, self.mpHands.HAND_CONNECTIONS, drawSpecsLm, drawSpecs)
        
        return img

    def findPosition(self, img, handNo=0):
        self.lmList = []
        xList = []
        yList = []
        self.bbox = []

        if self.results.multi_hand_landmarks:
            handLandmarks = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(handLandmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)

                xList.append(cx)
                yList.append(cy)

                self.lmList.append([id, cx, cy])
        
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
    
            self.bbox = xmin, ymin, xmax, ymax

        return self.lmList, self.bbox

    def fingersUp(self):
        fingers = []

        #thumb
        if self.lmList[self.tipIds[0]][2]<self.lmList[self.tipIds[0]+1][2]:
            fingers.append(1)
        else:
            fingers.append(0)
        
        #fingers
        for id in range(1,5):
            if self.lmList[self.tipIds[id]][2]<self.lmList[self.tipIds[id]-1][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=10, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        if draw:
            cv2.line(img, (x1,y1), (x2,y2), (255,0,255), t)
            cv2.circle(img, (x1,y1), r, (255,0,255), cv2.FILLED)
            cv2.circle(img, (x2,y2), r, (255,0,255), cv2.FILLED)
            cv2.circle(img, (cx,cy), r, (255,0,0), cv2.FILLED)
        
        length = math.hypot(x2-x1,y2-y1)

        return length, img, [x1,y1,x2,y2,cx,cy]
 


def main():
    cap = cv2.VideoCapture(0)
    cTime = 0
    pTime = 0
    detector = handDetector()
    while True:

        success, img = cap.read()
        img = detector.findHands(img)
        pos, bbox = detector.findPosition(img)
        if pos:
            print(detector.fingersUp())
            # res = detector.findDistance(4,8,img)

        cTime = time.time()
        fps = 1/ (cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),3)

        cv2.imshow("image",img)

        k = cv2.waitKey(1) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break

if __name__=="__main__":
    main()