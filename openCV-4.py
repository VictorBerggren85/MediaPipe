import cv2 as cv
import numpy as np
print(cv.__version__)

boardSize=int(800)
numSquares=int(8)
squareSize=boardSize/numSquares
dark=(0,0,0)
light=(0,0,255)
nowColor=dark

while 1:
    frame=np.zeros([boardSize,boardSize,3],dtype=np.uint8)

    for row in range(0,numSquares):
        for col in range(0,numSquares):
            frame[int(squareSize*row):int(squareSize*(row+1)),int(squareSize*col):int(squareSize*(col+1))]=nowColor
            if nowColor==dark:
                nowColor=light
            else:
                nowColor=dark
        if nowColor==dark:
            nowColor=light
        else:
            nowColor=dark
        
    cv.imshow('test',frame)
    cv.moveWindow('test',50,50)

    if cv.waitKey(1)&0xff==ord('q'):
        break

cv.destroyAllWindows()
