import cv2 as cv
import mediapipe as mp
import time as t
from helperClasses import cvCap
from helperClasses import mpHands
import numpy as np
print(cv.__version__)

w = 640
h = 360
p = 25
fps = 30

cam=cvCap(0,w,h,fps)
ts = t.time()
fpsFilter=30
numFingersLeft=0
numFingersRight=0
findHands=mpHands()

def parseHandGesture(fingers):
    res=''
    if len(fingers) == 0:
        res='fist'
    if len(fingers)==2:
        if 5 and 9 in fingers:
            res='Peace'
        if 5 and 17 in fingers:
            res='horns'
    if len(fingers)==4:
        res='High five'
    return res

def countFingers(hand):
    num=0
    fingers=[]
    for idx in range(5,18,4):
        if hand[idx][1] > hand[idx+3][1]:
            fingers.append(idx)
            num=num+1
    return parseHandGesture(fingers), num

while True:
    frame=cam.getFrame()
    fps = 1/(t.time() - ts)
    fpsFilter=fpsFilter*.9+fps*.1
    ts=t.time()   

    labels, hands=findHands.Marks(frame, w, h)
    for label, hand in zip(labels, hands):
        if label[1]=='Left':
            gesture, numFingersLeft=countFingers(hand)
            cv.putText(frame, str(numFingersLeft)+gesture,hand[4], cv.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
        if label[1]=='Right':
            gesture, numFingersRight=countFingers(hand)
            cv.putText(frame, str(numFingersRight)+gesture,hand[4], cv.FONT_HERSHEY_SIMPLEX, 1, (0,0, 255), 2)

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

cam.destroy()
cv.destroyAllWindows()
