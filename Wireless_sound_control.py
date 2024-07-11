import cv2
import mediapipe as mp
import numpy as np
import math


from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

mpDraw = mp.solutions.drawing_utils
#mp_drawing_styles = mp.solutions.drawing_styles
mpHands = mp.solutions.hands

# volume.GetMute()
# volume.GetMasterVolumeLevel()
hands = mpHands.Hands(max_num_hands=1)
cap = cv2.VideoCapture(0)
valRange = volume.GetVolumeRange()
Minval=valRange[0]
Maxval=valRange[1]
p = volume.GetMasterVolumeLevel()
Vol = np.interp(p,[Minval,Maxval],[0,100])
q="VOLUME : "+str(int(Vol))
while True:
    success, img = cap.read() 
    img = cv2.flip(img,1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []
            for id, lm in enumerate(handLms.landmark):
                #print(id, lm)
                h , w , c = img.shape
                cx, cy =int(lm.x *w) , int(lm.y*h)
                #print(id, cx, cy)
                lmList.append([id, cx, cy])
                
            # print(lmList)
            mpDraw.draw_landmarks(img, handLms ,mpHands.HAND_CONNECTIONS)  

            if lmList:
                x1, y1 = lmList[4][1] , lmList[4][2]
                x2, y2 = lmList[8][1] , lmList[8][2]
                cv2.circle(img, (x1,y1) , 5 , (2,6,233) , cv2.FILLED)          
                cv2.circle(img, (x2,y2) , 5 , (2,6,233) , cv2.FILLED)
                cv2.line(img,(x1,y1),(x2,y2),(30,87,245),3)       

                length = math.hypot((x2-x1),(y2-y1))
                # print(length)
                valRange = volume.GetVolumeRange()
                Minval=valRange[0]
                Maxval=valRange[1]
                vol = np.interp(length,[50,300],[Minval,Maxval])
                volume.SetMasterVolumeLevel(vol,None)
                Vol = np.interp(length,[50,300],[0,100])
                # p = volume.GetMasterVolumeLevel()
                q="VOLUME : "+str(int(Vol))
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (260, 50)
    fontScale = 1
    color = (10, 10, 250)
    thickness = 2
    cv2.putText(img,q, org, font, fontScale, color, thickness, cv2.LINE_AA)
    cv2.imshow("Command plate", img)
    cv2.waitKey(1)
# rANGE 30 T0 300
# 30==>-96
# 300==>0
