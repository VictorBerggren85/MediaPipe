import cv2 as cv
print(cv.__version__)

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

ok, _ = cam.read()

while ok:
    ok, frame = cam.read()

    frame[140:220,280:360]=(0,0,0)
    
    cv.rectangle(
        frame,      #target 
        (250,180),  #pt1
        (390,220),  #pt2
        (0,255,0),  #color
        4)          #thickness
    
    cv.circle(
        frame,          #target 
        (100, 100),     #center
        40,             #radious
        (255,255,0),    #color
        -1)             #thickness (-1 = fill)
    
    cv.putText(
        frame,                      #target
        'test',                     #text
        (250, 90),                  #position
        cv.FONT_HERSHEY_COMPLEX,    #font 
        2,                          #size
        (50, 50, 50),               #color
        2)                          #Thickness

    cv.imshow('test', frame)
    cv.moveWindow('test', p, p)

    if cv.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
