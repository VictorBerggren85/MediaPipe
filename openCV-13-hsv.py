import numpy as np
import cv2 as cv

x = 180
y = 256

frame1 = np.zeros([y, x, 3], dtype=np.uint8)
frame2 = np.zeros([y, x, 3], dtype=np.uint8)

for row in range(0,256,1):
    for col in range(0,180,1):
        frame1[row][col] =(col,row,255)   
        frame2[row][col] =(col,255,row)   

cvt1 = cv.cvtColor(frame1,cv.COLOR_HSV2BGR)
cvt2 = cv.cvtColor(frame2,cv.COLOR_HSV2BGR)

while 1:
    cv.imshow('light', cvt1)
    cv.moveWindow('light', 25, 25)
    cv.imshow('dark', cvt2)
    cv.moveWindow('dark', 25, 425)
    if cv.waitKey(1)==ord('q'):
        break
    
cv.destroyAllWindows()
