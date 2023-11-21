import cv2 as cv
print(cv.__version__)

cam = cv.VideoCapture(0)
w = 640
h = 480
p = 25
ok, _ = cam.read()

while ok:
    ok, frame = cam.read()
    gFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('test', frame)
    cv.imshow('testG', gFrame)
    cv.imshow('test2', frame)
    cv.imshow('testG2', gFrame)
    cv.moveWindow('test', p, p)
    cv.moveWindow('testG', p+w, p)
    cv.moveWindow('test2', p+w, p+h)
    cv.moveWindow('testG2', p, p+h)

    if cv.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
