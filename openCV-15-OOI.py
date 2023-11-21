import cv2 as cv
import time as t
import numpy as np
print(cv.__version__)

w = 640
h = 360
p1 = 25
p2 = 25
fps = 30
myRad = 15
wTB = int(w/2)
hTB=int(h/2)
codec = cv.VideoWriter_fourcc(*'MJPG')

hueLow =150
hueHigh=150
satLow=150
satHigh=150
valLow=150
valHigh=150

def tb1(val):
    global hueLow
    hueLow=val
def tb2(val):
    global hueHigh
    hueHigh =val
def tb3(val):
    global satLow
    satLow =val
def tb4(val):
    global satHigh
    satHigh=val
def tb5(val):
    global valLow
    valLow=val
def tb6(val):
    global valHigh
    valHigh = val

cam = cv.VideoCapture(0, cv.CAP_DSHOW)
cam.set(cv.CAP_PROP_FRAME_WIDTH, w)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, h)
cam.set(cv.CAP_PROP_FPS, fps)
cam.set(cv.CAP_PROP_FOURCC, codec)

cv.namedWindow('test')
cv.namedWindow('TB')
cv.moveWindow('TB', w+50, 50)

cv.createTrackbar('Hue Low', 'TB', 10, 179, tb1)
cv.createTrackbar('Hue High', 'TB', 20, 179, tb2)
cv.createTrackbar('Sat Low', 'TB', 10, 255, tb3)
cv.createTrackbar('Sat High', 'TB', 10, 255, tb4)
cv.createTrackbar('Val Low', 'TB', 10, 255, tb5)
cv.createTrackbar('Val High', 'TB', 10, 255, tb6)


ok, _ = cam.read()
ts = t.time()
fpsFilter=30
once = True
while ok:
    ok, frame = cam.read()
    fps = 1/(t.time() - ts)
    fpsFilter=int(fpsFilter*.9+fps*.1)
    ts=t.time()   

    frameHSV=cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lb=np.array([hueLow,satLow, valLow])
    ub=np.array([hueHigh,satHigh, valHigh])
    mask= cv.inRange(frameHSV, lb, ub)
    obj = cv.bitwise_and(frame, frame, mask=mask)
    
    contours,_=cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for c in contours:
        area=cv.contourArea(c)
        if area >= 100:
            cv.drawContours(frame, [c], 0, (0,0,255),2)
            x,y,rw,rh=cv.boundingRect(c)
            cv.rectangle(frame, (x,y), (x+rw, y+rh),(255,255,255),1)
            p1=x
            py=y


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
    cv.moveWindow('test', p1, p2)

    cv.imshow('obj', obj)
    cv.moveWindow('obj', p1+w, p2+h+30)

    cv.imshow('mask', mask)
    cv.moveWindow('mask', p1, p2+h+30)

    if cv.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
