import math as m
import cv2 as cv
import mediapipe as mp
import time as t
from mpHand import mpHands
print(cv.__version__)

mp_hands = mp.solutions.hands
w = 640
h = 360
p = 25
fps = 30
codec = cv.VideoWriter_fourcc(*'MJPG')

cam = cv.VideoCapture(0, cv.CAP_DSHOW)
cam.set(cv.CAP_PROP_FRAME_WIDTH, w)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, h)
cam.set(cv.CAP_PROP_FPS, fps)
cam.set(cv.CAP_PROP_FOURCC, codec)

ok, _ = cam.read()
ts = t.time()
fpsFilter=30

myHands = mpHands(0, 0.5, 0.5)

while ok:
    ok, frame = cam.read()
    fps = 1/(t.time() - ts)
    fpsFilter=fpsFilter*.9+fps*.1
    ts=t.time()   

    handIndexLabel, hands = myHands.Marks(frame, w, h)

    for label, hand in zip(handIndexLabel, hands):
        for index in (4, 8, 12, 16, 20):
            if label[1] == 'Right':
                cv.circle(frame, hand[index], 5, (0,0,255,), 3)
            if label[1] == 'Left':
                cv.circle(frame, hand[index], 5, (255,0,0,), 3)

    cv.rectangle(
        frame,      #target 
        (0,0),      #pt1
        (w,35),     #pt2
        (0,0,0),    #color
        -1)         #thickness
    
    cv.putText(
        frame,                      #target
        'fps: '+str(fpsFilter),     #text
        (25, 25),                   #position
        cv.FONT_HERSHEY_COMPLEX,    #font 
        1,                          #size
        (255, 255, 255),            #color
        1)                          #Thickness

    cv.imshow('test', frame)
    cv.moveWindow('test', p, p)

    if cv.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
