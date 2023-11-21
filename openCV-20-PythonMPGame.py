import cv2 as cv
import time as t
from mpHand import mpHands
print(cv.__version__)

boardSize=150
boardColor=(0,255,0)
boardXPos=0
ballSize=25
ballSpeedX=1
ballSpeedY=1
ballColor=(0,0,255)
ballPosX=1
ballPosY=1

score=1

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

# def mainMenu(message):
#     result=0
#     waitUp=0
#     waitDown=0
#     thumbsUp=True
#     thumbsDown=False
#     upMessage='Thumbs up to run game'
#     downMessage='Thumbs down to quit'
#     ok, frame = cam.read()

#     while ok:
#         ok, frame = cam.read()
#         hands = findHands.Marks(frame, w, h)
#         if len(hands):
#             hand=hands[0]
#             if hand[1][1] > hand[2][1] and hand[2][1] > hand[3][1] and hand[3][1] > hand[4][1]:
#                 waitDown=0
#                 waitUp=waitUp+1
#             else:
#                 waitUp=waitUp-1

#             if hand[1][1] < hand[2][1] and hand[2][1] < hand[3][1] and hand[3][1] < hand[4][1]:
#                 waitUp=0
#                 waitDown=waitDown+1
#             else:
#                 waitDown=waitDown-1
#         else:
#             waitUp=0
#             waitDown=0

#         cv.putText(
#             frame,                      #target
#             message,                    #text
#             (25, int(h/2)),             #position
#             cv.FONT_HERSHEY_COMPLEX,    #font 
#             1,                          #size
#             (255, 255, 255),            #color
#             1)                          #Thickness

#         cv.putText(
#             frame,                          #target
#             upMessage,                      #text
#             (25, 25),                       #position
#             cv.FONT_HERSHEY_COMPLEX,        #font 
#             1,                              #size
#             (255-waitUp, 255, 255-waitUp),  #color
#             1)                              #Thickness
#         cv.putText(
#             frame,                              #target
#             downMessage,                        #text
#             (25, 75),                           #position
#             cv.FONT_HERSHEY_COMPLEX,            #font 
#             1,                                  #size
#             (255-waitDown, 255-waitDown, 255),  #color
#             1)                                  #Thickness

#         cv.imshow('MainMenu', frame)
#         cv.moveWindow('MainMenu', p, p)
#         if waitUp == 255:
#             result=thumbsUp
#             break
#         if waitDown == 255:
#             result=thumbsDown
#             break
#     cv.destroyWindow('MainMenu')
#     return result

def runGame(frame):
    global boardSize
    global boardColor
    global boardXPos
    global ballSize
    global ballSpeedX
    global ballSpeedY
    global ballColor
    global ballPosX
    global ballPosY
    global score

    gameover = False
    changeMovementLeft = ballPosX+ballSize+ballSpeedX+ballSize >= w
    changeMovementRight = ballPosX+ballSize+ballSpeedX-ballSize <= 0
    changeMovementDown = ballPosY+ballSize+ballSpeedY-ballSize <= 0
    changeMovementUp = (ballPosY+ballSize+ballSpeedY+ballSize >= h-10) and (ballPosX < boardXPos+int(ballSize/2) and ballPosX-int(ballSize/2) < boardXPos)

    cv.circle(frame, (ballPosX+ballSize,ballPosY+ballSize), ballSize, ballColor, -1)

    if changeMovementLeft or changeMovementRight:
        ballSpeedX = ballSpeedX*-1
    if  changeMovementDown:
        ballSpeedY = ballSpeedY*-1
    if changeMovementUp:
        if ballSpeedY < 0:
            ballSpeedY = abs(ballSpeedY)
        else:
            ballSpeedY = ballSpeedY*-1
        score = score+1

    if ballPosY < h-10:
        gameover = True

    hands=findHands.Marks(frame, w, h)
    if len(hands) > 0:
        boardXPos=hands[0][8][0]
        cv.rectangle(frame, (int(boardXPos-boardSize/2), h-10), (int(boardXPos+boardSize/2), h), boardColor, -1)

    ballPosX=ballPosX+ballSpeedX*score
    ballPosY=ballPosY+ballSpeedY*score
    
    cv.putText(
        frame,                      #target
        'Score:'+str(score-1),      #text
        (25, 25),                   #position
        cv.FONT_HERSHEY_COMPLEX,    #font 
        1,                          #size
        (255, 255, 255),            #color
        1)                          #Thickness
    return (gameover, frame)

findHands=mpHands()

ok, _ = cam.read()
# run=mainMenu('Start Game')
run = True

while ok and run:
    gameover=False
    ok, frame = cam.read()
 
    if gameover:
        # cv.destroyWindow('game')
        # run=mainMenu('final score: '+str(score))
        print('Final score:'+str(score-1))
    else: 
        gameover, frame = runGame(frame)

    cv.imshow('game', frame)
    cv.moveWindow('game', p, p)

    if cv.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
