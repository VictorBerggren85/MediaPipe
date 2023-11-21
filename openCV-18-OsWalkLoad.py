import face_recognition as fr
import cv2 as cv
import os
import time as t
import pickle as pkl
print(cv.__version__)

w = 640
h = 360
p = 25
fps = 30
codec = cv.VideoWriter_fourcc(*'MJPG')

roiW = 150
roiH = 50
pos = [0,0]
moveW = 1
moveH = 1
font=cv.FONT_HERSHEY_SIMPLEX

with open('trainingData.pkl', 'rb') as fo:
    Encodings=pkl.load(fo)
    Names=pkl.load(fo)

fo.close()

cam = cv.VideoCapture(0, cv.CAP_DSHOW)
cam.set(cv.CAP_PROP_FRAME_WIDTH, w)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, h)
cam.set(cv.CAP_PROP_FPS, fps)
cam.set(cv.CAP_PROP_FOURCC, codec)

ok, _ = cam.read()
ts = t.time()
fpsFilter=30

while ok:
    ok, frame = cam.read()
    fps = 1/(t.time() - ts)
    fpsFilter=int(fpsFilter*.9+fps*.1)
    ts=t.time()   

    frameRGB=cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    faceLocations=fr.face_locations(frameRGB)
    unknownEncodings=fr.face_encodings(frameRGB, faceLocations)

    for (top,right,bottom,left), unknownEncodings in zip(faceLocations, unknownEncodings):
        cv.rectangle(frame, (left,top),(right,bottom),(255,0,0),2)
        name ='unknown'
        matches=fr.compare_faces(Encodings, unknownEncodings)
        if True in matches:
            i=matches.index(True)
            name=Names[i]
        cv.rectangle(frame, (left,top-10),(right,top),(255,0,0),-1)
        cv.putText(frame, name, (left, top-2),font,.3,(255,255,255),1)

    cv.rectangle(
        frame,      #target 
        (0,0),      #pt1
        (w,35),     #pt2
        (0,0,0),    #color
        -1)         #thickness
    
    cv.putText(
        frame,                      #target
        'fps: '+str(fpsFilter),     #text
        (25, 26),                   #position
        font,                       #font 
        1,                          #size
        (255, 255, 255),            #color
        1)                          #Thickness
    
    cv.putText(
        frame,                      #target
        'Pos: '+str(pos),           #text
        (200, 26),                  #position
        font,                       #font 
        1,                          #size
        (255, 255, 0),              #color
        1)                          #Thickness

    cv.imshow('test', frame)
    cv.moveWindow('test', p, p)

    if cv.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
