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
lowLim=0
hiLim=468

def setLow(val):
    global lowLim
    lowLim=val
def setHi(val):
    global hiLim
    hiLim=val

cam=cvCap(0,w,h,fps)
ts = t.time()
fpsFilter=30

faceMesh=mpFaceMesh()

cv.namedWindow('Trackbars')
cv.createTrackbar('lowLimit', 'Trackbars', 0,468, setLow)
cv.createTrackbar('HiLimit', 'Trackbars', 468,468, setHi)
cv.moveWindow('Trackbars', p+w, p)
cv.resizeWindow('Trackbars', 400, 50)

while True:
    frame=cam.getFrame()
    fps = 1/(t.time() - ts)
    fpsFilter=fpsFilter*.9+fps*.1
    ts=t.time()   

    sizeFactor=4

    mesh=faceMesh.Marks(frame, w, h)
    idx = 0
    for point in mesh:
        if idx>=lowLim and idx<=hiLim:
            cv.circle(frame, point, 1, (0, 255, 0))
        idx=idx+1
        
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
