import cv2 as cv
import mediapipe as mp
import time as t
from helperClasses import cvCap
from helperClasses import mpFaceMesh
import numpy as np
print(cv.__version__)

w = 640
h = 360
p = 25
fps = 30

cam=cvCap(0,w,h,fps)
ts = t.time()
fpsFilter=30

faceMesh=mpFaceMesh()

while True:
    frame=cam.getFrame()
    fps = 1/(t.time() - ts)
    fpsFilter=fpsFilter*.9+fps*.1
    ts=t.time()   

    sizeFactor=4
    meshFrame=np.zeros((int(w*sizeFactor), int(h*sizeFactor)), np.uint8)

    mesh=faceMesh.Marks(frame, w, h)
    indx=0
    for lm in mesh:
        cv.putText(meshFrame, str(indx), (int(lm[0]*sizeFactor), int(lm[1]*sizeFactor)), cv.FONT_HERSHEY_COMPLEX, 0.3, (255,255,255), 1)
        indx = indx+1

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
    cv.imshow('mesh', meshFrame)
    cv.moveWindow('mesh', p+w, p)
    if cv.waitKey(1) & 0xff == ord('q'):
        break

cam.destroy()
cv.destroyAllWindows()
