import cv2
from random import randrange

trained_faces_data = cv2.CascadeClassifier("FaceRecognition\haarcascade_frontalface_default.xml")

img = cv2.imread('FaceRecognition\\img.webp')

grayscaled_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

face_coordinates = trained_faces_data.detectMultiScale(grayscaled_img)

for (x,y,w,h) in face_coordinates:
    cv2.rectangle(img,(x,y),(x+w,y+h),(randrange(256),randrange(256),randrange(256)),4)
    print(x,y,w,h)


cv2.imshow("face detection tool",img)
cv2.waitKey()
