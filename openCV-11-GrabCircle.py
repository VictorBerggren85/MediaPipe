import cv2 as cv
import time as t
import math as m
import numpy as np
print(cv.__version__)


def trackbarCB(val):
    global wTB
    wTB = val

def trackbar2CB(val):
    global hTB
    hTB = val

def trackbar3CB(val):
    global myRad
    myRad = val

w = 640
h = 360
p = 25
fps = 30
myRad = 15
wTB = int(w/2)
hTB=int(h/2)
codec = cv.VideoWriter_fourcc(*'MJPG')

cam = cv.VideoCapture(0, cv.CAP_DSHOW)
cam.set(cv.CAP_PROP_FRAME_WIDTH, w)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, h)
cam.set(cv.CAP_PROP_FPS, fps)
cam.set(cv.CAP_PROP_FOURCC, codec)

cv.namedWindow('test')
cv.namedWindow('Trackbars')
cv.resizeWindow('Trackbars', 400, 120)
cv.moveWindow('Trackbars', w+50, 50)
cv.createTrackbar('xPos', 'Trackbars', int(w/2), w, trackbarCB)
cv.createTrackbar('yPos', 'Trackbars', int(h/2), h, trackbar2CB)
cv.createTrackbar('rad', 'Trackbars', myRad, h, trackbar3CB)


ok, _ = cam.read()
ts = t.time()
fpsFilter=30
once = True
while ok:
    ok, frame = cam.read()
    fps = 1/(t.time() - ts)
    fpsFilter=int(fpsFilter*.9+fps*.1)
    ts=t.time()   

    p1 = (wTB-myRad,hTB-myRad)
    p2 = (wTB+myRad,hTB+myRad)
    
    if wTB-myRad > 0 and hTB-myRad > 0 and wTB+myRad < w and hTB+myRad < h:
        roiC = np.zeros([(wTB+myRad)-(wTB-myRad),(hTB+myRad)-(hTB-myRad), 3], dtype=np.uint8)
        roi = frame[hTB-myRad:hTB+myRad,wTB-myRad:wTB+myRad]
        for x in range(wTB-myRad, wTB+myRad):
            for y in range(hTB-myRad, hTB+myRad):
                if m.sqrt(pow(wTB-x,2)+pow(hTB-y,2)) < myRad:
                    roiC[x-(wTB-myRad)][y-(hTB-myRad)]=roi[x-(wTB-myRad)][y-(hTB-myRad)]

        cv.imshow('roi', roiC)


    cv.moveWindow('roi', 500, 500)
    cv.circle(frame, (wTB, hTB), myRad, (0,255,0), 2)

    roi = frame[:,:]

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
