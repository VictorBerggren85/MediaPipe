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

cam = cv.VideoCapture(0, cv.CAP_DSHOW)
cam.set(cv.CAP_PROP_FRAME_WIDTH, w)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, h)
cam.set(cv.CAP_PROP_FPS, fps)
cam.set(cv.CAP_PROP_FOURCC, codec)

faceFrontCascade=cv.CascadeClassifier(r'C:/Users/es017590\Documents/py/HAAR/haarcascade_frontalface_default.xml')
faceProfileCascade=cv.CascadeClassifier(r'C:/Users/es017590\Documents/py/HAAR/haarcascade_profileface.xml')
leftEyeCascade=cv.CascadeClassifier(r'C:/Users/es017590\Documents/py/HAAR/haarcascade_lefteye_2splits.xml')
rightEyeCascade=cv.CascadeClassifier(r'C:/Users/es017590\Documents/py/HAAR/haarcascade_righteye_2splits.xml')

ok, _ = cam.read()
ts = t.time()
t.sleep(.1)
fpsFilter=30
once = True
while ok:
    ok, frame = cam.read()
    fps = 1/(t.time() - ts)
    fpsFilter=int(fpsFilter*.9+fps*.1)
    ts=t.time()   

    frameGray=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces=faceFrontCascade.detectMultiScale(frameGray,1.3,5)
    profiles=faceProfileCascade.detectMultiScale(frameGray, 1.3,5)

    if len(profiles):
        for xp,yp,wp,hp in profiles:
            profile=frameGray[yp:yp+hp,xp:xp+wp]
            lEyes=leftEyeCascade.detectMultiScale(profile, 1.3,5)
            rEyes=rightEyeCascade.detectMultiScale(profile, 1.3,5)
            if len(lEyes):
                for xe,ye,we,he in lEyes:
                    # cv.rectangle(frame, (xp+xe, yp+ye), (xp+xe+we,yp+ye+he), (0,255,0), 2)
                    cv.circle(frame, (xp+xe+int(we/2), yp+ye+int(he/2)), 5, (0,255,0), -1)
            if len(rEyes):
                for xer,yer,wer,her in rEyes:
                    # cv.rectangle(frame, (xp+xer, yp+yer), (xp+xer+wer,yp+yer+her), (0,255,0), 2)        
                    cv.circle(frame, (xp+xer+int(wer/2), yp+yer+int(her/2)), 5, (0,255,0), -1)
            
            cv.rectangle(frame, (xp, yp), (xp+wp,yp+hp), (0,255,0), 2)

    if len(faces):
        for xf,yf,wf,hf in faces:
            face=frameGray[yf:yf+hf,xf:xf+wf]
            lEyes=leftEyeCascade.detectMultiScale(face, 1.3,5)
            rEyes=rightEyeCascade.detectMultiScale(face, 1.3,5)
            if len(lEyes):
                for xe,ye,we,he in lEyes:
                    # cv.rectangle(frame, (xf+xe, yf+ye), (xf+xe+we,yf+ye+he), (0,255,0), 2)
                    cv.circle(frame, (xf+xe+int(we/2), yf+ye+int(he/2)), 5, (0,255,0), -1)
            if len(rEyes):
                for xer,yer,wer,her in rEyes:
                    # cv.rectangle(frame, (xf+xer, yf+yer), (xf+xer+wer,yf+yer+her), (0,255,0), 2)        
                    cv.circle(frame, (xf+xer+int(wer/2), yf+yer+int(her/2)), 5, (0,255,0), -1)
            cv.rectangle(frame, (xf, yf), (xf+wf,yf+hf), (0,255,0), 2)

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

    if cv.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
