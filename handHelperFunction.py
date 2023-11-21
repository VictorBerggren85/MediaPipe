import math as m
import cv2 as cv
import mediapipe as mp
import time as t
print(cv.__version__)

w = 640
h = 360
p = 25
fps = 30
toggle = False
codec = cv.VideoWriter_fourcc(*'MJPG')

hands=mp.solutions.hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

def parseLandmarks(frame):
    myHands=[]
    frameRGB=cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results=hands.process(frameRGB)
    if results.multi_hand_landmarks != None:
        for handLandmarks in results.multi_hand_landmarks:
            myHand=[]
            for landMark in handLandmarks.landmark:
                myHand.append((int(landMark.x*w), int(landMark.y*h)))
            myHands.append(myHand)
    return myHands
  
cam = cv.VideoCapture(0, cv.CAP_DSHOW)
cam.set(cv.CAP_PROP_FRAME_WIDTH, w)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, h)
cam.set(cv.CAP_PROP_FPS, fps)
cam.set(cv.CAP_PROP_FOURCC, codec)

mpDraw=mp.solutions.drawing_utils

ok, _ = cam.read()
ts = t.time()
fpsFilter=30
diam=1

while ok:
    ok, frame = cam.read()
    fps = 1/(t.time() - ts)
    fpsFilter=fpsFilter*.9+fps*.1
    ts=t.time()   
    myHands=parseLandmarks(frame)
    for hand in myHands:
        cv.circle(frame, (hand[20][0],hand[20][1]), (10), (255,0,0),2)
        # cv.circle(frame, (hand[16][0],hand[16][1]), (10), (255,0,0),2)
        # cv.circle(frame, (hand[12][0],hand[12][1]), (10), (255,0,0),2)
        # cv.circle(frame, (hand[8][0],hand[8][1]), (10), (255,0,0),2)
        # cv.circle(frame, (hand[4][0],hand[4][1]), (10), (255,0,0),2)

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
