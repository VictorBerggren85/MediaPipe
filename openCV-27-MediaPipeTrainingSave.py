import cv2 as cv
import math as m
import time as t
from helperClasses import cvCap
from helperClasses import mpHands
import pickle as pkl
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
trainName=''
gestures=[]

numGest=int(input('Number of gesures to train (0 to quit): '))
if numGest:
    for g in range(0,numGest,1):
        gestures.append(input('name gesture # '+str(g+1)+': '))

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

# Saving
trainName=input('filename (Leave empty for for default): ')
if trainName=='':
    trainName='default'
trainName=trainName+'.pkl'
with open(trainName,'wb') as f:
    pkl.dump(gestures,f)
    pkl.dump(trainingData,f)

cam.destroy()
cv.destroyAllWindows()
