import cv2 as cv
import time as t
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

    frameROI = frame[pos[0]:roiH+pos[0],pos[1]:roiW+pos[1]]
    gRoi = cv.cvtColor(frameROI, cv.COLOR_BGR2GRAY)
    gRoiBGR = cv.cvtColor(gRoi, cv.COLOR_GRAY2BGR)
    frame[pos[0]:roiH+pos[0],pos[1]:roiW+pos[1]] = gRoiBGR

    if roiH+pos[0]+moveH == h or pos[0]+moveH < 0:
        moveH = moveH*-1
    if roiW+pos[1]+moveW == w or pos[1]+moveW < 0:
        moveW = moveW*-1

    pos[0] = pos[0]+moveH
    pos[1] = pos[1]+moveW

    cv.imshow('roi', frameROI)
    cv.imshow('roi gray', gRoi)
    cv.moveWindow('roi', w+50, 25)
    cv.moveWindow('roi gray', w+50, 125)

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
    
    cv.putText(
        frame,                      #target
        'Pos: '+str(pos),           #text
        (200, 26),                  #position
        cv.FONT_HERSHEY_COMPLEX,    #font 
        1,                          #size
        (255, 255, 0),            #color
        1)                          #Thickness

    cv.imshow('test', frame)
    cv.moveWindow('test', p, p)

    if cv.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
