import math as m
import cv2 as cv
import mediapipe as mp
import time as t
print(cv.__version__)
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles
w = 640
h = 360
p = 25
fps = 30
toggle = False
codec = cv.VideoWriter_fourcc(*'MJPG')

def parseHandData(hands_landmarks):
    hand = []
    global toggle
    for hand_landmarks in hands_landmarks.landmark:
        hand.append((int(hand_landmarks.x*w), int(hand_landmarks.y*h)))
    if(hand[4][0]-hand[8][0]<10 and hand[4][1]-hand[8][1]<10 and not toggle):
        toggle=True 
    return hand

cam = cv.VideoCapture(0, cv.CAP_DSHOW)
cam.set(cv.CAP_PROP_FRAME_WIDTH, w)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, h)
cam.set(cv.CAP_PROP_FPS, fps)
cam.set(cv.CAP_PROP_FOURCC, codec)

mpDraw=mp.solutions.drawing_utils

ok, _ = cam.read()
ts = t.time()
fpsFilter=30
diam=1

hands = mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

while ok:
    ok, frame = cam.read()
    fps = 1/(t.time() - ts)
    fpsFilter=fpsFilter*.9+fps*.1
    ts=t.time()   
    hand = []
    frameBGR=cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results=hands.process(frameBGR)
    if results.multi_hand_landmarks != None:
        for hand_landmarks in results.multi_hand_landmarks:
            hand = parseHandData(hand_landmarks)
            # mpDraw.draw_landmarks(
            #     frame,
            #     hand_landmarks,
            #     mp_hands.HAND_CONNECTIONS,
            #     mp_drawing_styles.get_default_hand_landmarks_style(),
            #     mp_drawing_styles.get_default_hand_connections_style())
    if toggle:
        measure = int(m.sqrt(pow((hand[4][0]-hand[8][0]),2)+pow((hand[4][1]-hand[8][1]),2)))
        diam = diam*.9+measure*.1
        cv.circle(frame, hand[4], (int(diam)), (200,0,0),-1)

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
