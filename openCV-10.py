import cv2 as cv
import time as t
print(cv.__version__)

event = [0, 0, 0]
mark = False
enlarge = 1
slow = 0

def mouseClick(e, xPos, yPos, flags, params):
    global event
    event = [e, xPos, yPos]

w = 640
h = 360
p = 25
fps = 30
codec = cv.VideoWriter_fourcc(*'MJPG')

cam = cv.VideoCapture(0, cv.CAP_DSHOW)
cam.set(cv.CAP_PROP_FRAME_WIDTH, w)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, h)
cam.set(cv.CAP_PROP_FPS, fps)
cam.set(cv.CAP_PROP_FOURCC, codec)

cv.namedWindow('test')
cv.namedWindow('roi')
cv.setMouseCallback('test', mouseClick)

ok, _ = cam.read()
ts = t.time()
fpsFilter=30

while ok:
    ok, frame = cam.read()
    fps = 1/(t.time() - ts)
    fpsFilter=int(fpsFilter*.9+fps*.1)
    ts=t.time()   


    if event[0]==1:
        mark = True
    if event[0]==4:
        mark = False
        roi=frame[event[2]-enlarge:event[2]+enlarge,event[1]-enlarge:event[1]+enlarge]
        cv.imshow('roi', roi)
        cv.moveWindow('roi', w+50, 50)
        enlarge = 1

    if event[0] == 5:
        cv.destroyWindow('roi')
        roi=[]
        enlarge = 1
        event[0]=0

    if mark:
        cv.rectangle(
            frame, 
            (event[1]-enlarge,event[2]-enlarge),
            (event[1]+enlarge,event[2]+enlarge),
            (255,0,0),
            1)

    if enlarge < 51 and slow%3 == 1:
        enlarge=enlarge+1
    slow = slow+1

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
