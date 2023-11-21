import cv2 as cv
import math as m
import time as t
from helperClasses import cvCap
from helperClasses import mpHands
import pickle as pkl
import numpy as np
import serial
print(cv.__version__)

w = 640
h = 360
p = 25
fps = 30

arduinoData=serial.Serial('COM3', 115200)

cam=cvCap(0,w,h,fps)
ts = t.time()
fpsFilter=30
findHands=mpHands()
trainName=''

gestures=[]
trainingData=[]
tol=25
keyPoints=[0,4,5,8,9,12,13,16,17,20]

def send(gesture):
    gesture=gesture+'\r'
    arduinoData.write(gesture.encode())

def compareDatasets(knownData, unknownData, keypoints):
    error=0
    if len(knownData) and len(unknownData):
        for row in keypoints:
            for col in keypoints:
                error=error+abs(knownData[row][col]-unknownData[row][col])    
    return error

def calculateDistanceBetweenAllPoints(hand):
    measuredDistances=np.zeros((21,21),np.float16)
    palmSize=m.sqrt(abs(pow(hand[0][0],2)-pow(hand[9][0],2)))+m.sqrt(abs(pow(hand[0][1],2)-pow(hand[9][1],2)))
    for row in range(0,21):
        for col in range(0,21):
            pt1=m.sqrt(abs(pow(hand[row][0],2)-pow(hand[col][0],2)))
            pt2=m.sqrt(abs(pow(hand[row][1],2)-pow(hand[col][1],2)))
            measuredDistances[row][col]=int((pt1+pt2)/palmSize)
    return measuredDistances

def findGesture(unknownGesture, knownGesture, keyPoints, gestures, tol):
    errorArr=[]
    errorMin=999999
    if knownGesture!=[] and unknownGesture!=[]:
        for i in range(0,len(gestures),1):
            errorArr.append(compareDatasets(knownGesture[i],unknownGesture,keyPoints))
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

# Loading
trainName=input('Input name of training data (Leave empty for for default): ')
if trainName=='':
    trainName='default'
trainName=trainName+'.pkl'
with open(trainName,'rb') as f:
    gestures=pkl.load(f)
    trainingData=pkl.load(f)

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

    send(gesture)

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
