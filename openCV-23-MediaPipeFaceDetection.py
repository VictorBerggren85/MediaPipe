import cv2 as cv
import mediapipe as mp
import time as t
from mpHand import mpFace
print(cv.__version__)

mp_hands = mp.solutions.hands
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

findFace=mpFace()

print('cv.CAP_PROP_FRAME_WIDTH', str(cv.CAP_PROP_FRAME_WIDTH))

ok, _ = cam.read()
ts = t.time()
fpsFilter=30

while ok:
    ok, frame = cam.read()
    fps = 1/(t.time() - ts)
    fpsFilter=fpsFilter*.9+fps*.1
    ts=t.time()   

    faces=findFace.Marks(frame, w, h)

    if len(faces):
        for face in faces:
            cv.rectangle(frame, face[0], face[1], (150,150,200), 3)

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

cam.release()
cv.destroyAllWindows()
