from re import X
import cv2
import numpy as np
import MainEngine.Vision.HandDetectionModule.handDetectionModule as htm
# import handDetectionModule as htm
import time
import autopy
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def virtualMouse(mode=False, maxhands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
    wCam, hCam = 640, 480
    wScr, hScr = autopy.screen.size()
    cap = cv2.VideoCapture(0)
    frameR = 175
    radius = 10
    thickness = 3
    smoothening = 5
    pLocX, pLocY = 0,0
    cLocX, cLocY = 0,0

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.GetMute()
    volume.GetMasterVolumeLevel()
    volRange = volume.GetVolumeRange()

    minVol = volRange[0]
    maxVol = volRange[1]

    cap.set(3,wCam)
    cap.set(4,hCam)

    cap = cv2.VideoCapture(0)
    cTime = 0
    pTime = 0
    detector = htm.handDetector(mode=mode, maxhands=maxhands, modelComplexity=modelComplexity, detectionCon=detectionCon, trackCon=trackCon)

    while True:

        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)

        if lmList:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            
            fingers = detector.fingersUp()
            
            cv2.rectangle(img, (frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255),thickness)

            #mouse movement mechanism
            if fingers[0]==0 and fingers[1]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0:
                x3 = np.interp(x1, (frameR, wCam-frameR), (0,wScr))
                y3 = np.interp(y1, (frameR, hCam-frameR), (0,hScr))

                cLocX, cLocY = pLocX + (x3 - pLocX) // smoothening, pLocY + (y3 - pLocY) // smoothening

                cv2.circle(img, (x1,y1), radius, (255,0,255), cv2.FILLED)
                try:
                    autopy.mouse.move(wScr-cLocX,cLocY)
                    pLocX, pLocY = cLocX, cLocY
                except Exception as err:
                    print
            
            #adjust volume mechanism max - 130, min - 60
            elif fingers[0]==1 and fingers[1]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0:
                length, img, lineInfo = detector.findDistance(4, 8, img)
                if length<25:
                    cv2.line(img, (x1,y1), (x2,y2), (0,0,255), thickness)
                    cv2.circle(img, (lineInfo[4],lineInfo[5]), radius, (0,0,255), cv2.FILLED)
                elif length>60:
                    cv2.line(img, (x1,y1), (x2,y2), (255,0,255), thickness)
                    cv2.circle(img, (lineInfo[4],lineInfo[5]), radius, (0,0,0), cv2.FILLED)
                vol = np.interp(length, [20,80], [minVol,maxVol])
                volume.SetMasterVolumeLevel(vol, None)


            #mouse click mechanism
            elif fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and fingers[3]==0 and fingers[4]==0:
                length, img, lineInfo = detector.findDistance(8, 12, img) 
                if length<20:
                    cv2.circle(img, (lineInfo[4],lineInfo[5]), radius, (0,255,0), cv2.FILLED)
                    autopy.mouse.click()

            #mouse scrolling mechanism
            #scroll up
            elif fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==0:
                pyautogui.scroll(-400)
            #scroll down
            elif fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1:
                pyautogui.scroll(400)

        cTime = time.time()
        fps = 1/ (cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),thickness)
        if bbox:
            xmin, ymin, xmax, ymax = bbox
            cv2.rectangle(img,(xmin-20,ymin-20),(xmax+20,ymax+20),(0,255,0),thickness)

        cv2.imshow("image",img)

        k = cv2.waitKey(1) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break

# virtualMouse()

