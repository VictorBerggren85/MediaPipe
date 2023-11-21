import cv2 as cv
import math as m
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
findHands=mpHands()

gestures=['fist', 'open', 'peace', 'spok', 'horns']
trainingData=[]
tol=2000
stillTraining=len(gestures)
keyPoints=[0,4,5,8,9,12,13,16,17,20]

def compareDatasets(knownData, unknownData, keypoints):
    error=0
    if len(knownData) and len(unknownData):
        for row in keypoints:
            for col in keypoints:
                error=error+abs(knownData[row][col]-unknownData[row][col])    
    return error

def calculateDistanceBetweenAllPoints(hand):
    measuredDistances=np.zeros((21,21),np.float16)
    z=0
    for row in range(0,21):
        for col in range(0,21):
            z=z+hand[row][2]/1000
    for row in range(0,21):
        for col in range(0,21):
            pt1=m.sqrt(abs(pow(hand[row][0],2)-pow(hand[col][0],2)))
            pt2=m.sqrt(abs(pow(hand[row][1],2)-pow(hand[col][1],2)))
            measuredDistances[row][col]=int((pt1+pt2)/(z))
    return measuredDistances

def findGesture(unknownGesture, knownGesture, keyPoints, gestures, tol):
    errorArr=[]
    if knownGesture!=[] and unknownGesture!=[]:
        for i in range(0,len(gestures),1):
            errorArr.append(compareDatasets(knownGesture[i],unknownGesture,keyPoints))
        errorMin=999999
        minIndex=0
        for i in range(0,len(errorArr),1):
            if errorArr[i]<errorMin:
                errorMin=errorArr[i]
                minIndex=i
        if errorMin<tol:
            gesture=gestures[minIndex]
        else:
            gesture='unknown'
    else:
        gesture='unknown'
    return (gesture, errorMin)

while stillTraining: # Train
    frame=cam.getFrame()
    cv.rectangle(
        frame,                  #target 
        (int(w/4),int(h/4)),    #pt1
        (int(w/2),int(w/2)),    #pt2
        (0,255,255),            #color
        4)                      #thickness

    cv.putText(
        frame,                                                                      #target
        'Make '+gestures[len(gestures)-(stillTraining)]+' in square ans press t',   #text
        (int(w/4)-5,int(h/4)-5),                                                    #position
        cv.FONT_HERSHEY_COMPLEX,                                                    #font 
        .5,                                                                         #size
        (55, 55, 55),                                                               #color
        1)                                                                          #Thickness

    cv.imshow('train', frame)
    cv.moveWindow('train',p,p)

    if cv.waitKey(1)==ord('t'):
        _, hands=findHands.Marks(frame,w,h)
        if hands!=[]:
            trainingData.append(calculateDistanceBetweenAllPoints(hands[0]))
        stillTraining=stillTraining-1
cv.destroyAllWindows()

while True: #Run
    frame=cam.getFrame()
    fps = 1/(t.time() - ts)
    fpsFilter=fpsFilter*.9+fps*.1
    ts=t.time()   
    gesture=''
    smallestDiff=0
    errorMeasures=[]
    _, hands=findHands.Marks(frame,w,h)
    if hands!=[]:
        unknownData=calculateDistanceBetweenAllPoints(hands[0])
        gesture, smallestDiff=findGesture(unknownData, trainingData, keyPoints, gestures, tol)

    cv.rectangle(
        frame,                  #target 
        (int(w/4),int(h/4)),    #pt1
        (int(w/2),int(w/2)),    #pt2
        (0,255,0),              #color
        4)                      #thickness

    cv.putText(
        frame,                      #target
        gesture+' '+str(smallestDiff),  #text
        (int(w/4)-5,int(h/4)-5),    #position
        cv.FONT_HERSHEY_COMPLEX,    #font 
        .5,                         #size
        (0, 255, 0),                #color
        1)                          #Thickness

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
    t. sleep(.01)

cam.destroy()
cv.destroyAllWindows()
