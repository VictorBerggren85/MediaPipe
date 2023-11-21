import cv2 as cv
import time as t
import math as m
import numpy as np
print(cv.__version__)

w = 640
h = 360
pX = 25
pY = 25
fps = 30
myRad = 15
wTB = int(w/2)
hTB=int(h/2)
codec = cv.VideoWriter_fourcc(*'MJPG')
mouseEvent = (0,0,0)

cam = cv.VideoCapture(0, cv.CAP_DSHOW)
cam.set(cv.CAP_PROP_FRAME_WIDTH, w)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, h)
cam.set(cv.CAP_PROP_FPS, fps)
cam.set(cv.CAP_PROP_FOURCC, codec)

def mouseClick(e, x, y, f, p):
    global mouseEvent
    mouseEvent = (e, x, y)

def trackbarCB(val):
    cam.set(cv.CAP_PROP_FRAME_WIDTH, val)
    cam.set(cv.CAP_PROP_FRAME_HEIGHT, int(9/16*val))

def trackbar2CB(val):
    global pX
    pX = val

def trackbar3CB(val):
    global pY
    pY = val

cv.namedWindow('test')
cv.namedWindow('Trackbars')
cv.resizeWindow('Trackbars', 400, 200)
cv.moveWindow('Trackbars', w+50, 50)
cv.createTrackbar('Size', 'Trackbars', int(w), w*2, trackbarCB)
cv.createTrackbar('X Move', 'Trackbars', pX, 1000, trackbar2CB)
cv.createTrackbar('Y Move', 'Trackbars', pY, 1000, trackbar3CB)

cv.setMouseCallback('test', mouseClick)

ok, _ = cam.read()
ts = t.time()
fpsFilter=30
once = True
while ok:
    ok, frame = cam.read()
    fps = 1/(t.time() - ts)
    fpsFilter=int(fpsFilter*.9+fps*.1)
    ts=t.time()   

    if mouseEvent[0] == 1:
        x=mouseEvent[1]
        y=mouseEvent[2]
        colorFrame=np.zeros([50,50,3], dtype=np.uint8)
        clr = frame[y][x]
        colorFrame[:,:]=clr
        cv.imshow('testC',colorFrame)
        cv.moveWindow('testC', w+50, 300)

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
    cv.moveWindow('test', pX, pY)

    if cv.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
