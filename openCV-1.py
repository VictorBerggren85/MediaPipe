import cv2 as cv
print(cv.__version__)

cam = cv.VideoCapture(0)
p = 25
ok, _ = cam.read()

while ok:
    ok, frame = cam.read()

    cv.imshow('test', frame)
    cv.moveWindow('test', p, p)

    if cv.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
