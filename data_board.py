import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm
from DataBoard.HandTrackingModule import handDetector
import webbrowser

thickness_brush = 15
eraser_thickness = 50
ext_board = np.zeros((500, 1280, 3), dtype='uint8')
xp=0
yp=0

overlayList = []
folderDir = "canva_top_part"
myList = os.listdir(folderDir)
color=(255,255,255)
print(myList)

for imPath in myList:
    image = cv2.imread(f'{folderDir}/{imPath}')
    overlayList.append(image)

top = overlayList[0]
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,500)

detector: handDetector = htm.handDetector(detectionCon=0.9)

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)


# Landmarks
    img = detector.findHands(img)
    lmList, box= detector.findPosition(img)
    if len(lmList)!=0:
        print(lmList)

        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1) For checking click area....
        #fingerUp
        fingers= detector.fingersUp()
        print(fingers)

        #selection mode
        if fingers[1] and fingers[2]:
            cv2.rectangle(img, (x1,y1-30), (x2,y2+30),(255,0,255),cv2.FILLED)
            xp, yp = 0, 0
            print("Selecting")

            if y1<150:
                if x1<255:
                    webbrowser.open('iamdata.co.in')
                if 290<x1<445 :
                    top=overlayList[0]
                    color =(50,50,200)
                if 470<x1<600 :
                    top=overlayList[1]
                    color =(255,60,60)
                if 620<x1<730 :
                    top=overlayList[2]
                    color = (50,200,50)
                if 740<x1<880 :
                    top=overlayList[3]
                    color =(0, 0, 0)



        # drawing mode
        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1),15,color,cv2.FILLED )
            print("drawing..")


            if xp ==0 and yp ==0:
                xp = x1
                yp = y1



            # External BOARD
            if color==(0,0,0):
                cv2.line(img, (xp,yp),(x1,y1),color,eraser_thickness)
                cv2.line(ext_board, (xp,yp),(x1,y1),color,eraser_thickness)

            else:
                cv2.line(img, (xp,yp),(x1,y1),color,thickness_brush)
                cv2.line(ext_board, (xp,yp),(x1,y1),color,thickness_brush)



            xp= x1
            yp= y1

        # Clear screenp
        if all(x >= 1 for x in fingers):
            ext_board = np.zeros((500, 1280, 3),  dtype='uint8')


    # Clear black and white
    # imgGray = cv2.cvtColor(ext_board, cv2.COLOR_RGB2GRAY)
    # _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    # imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2RGB)
    # img = cv2.bitwise_and(img, imgInv)
    # img = cv2.bitwise_or(img, ext_board)


    # Overlay
    img[0:150,0:1280]= top
    # img = cv2.addWeighted(img,0.5,ext_board,0.5,0)

    cv2.imshow("image" ,img)
    cv2.imshow("image2" ,ext_board)

    cv2.waitKey(1)