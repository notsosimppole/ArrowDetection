import cv2
import numpy as np
import math

#img = cv2.imread(r"C:\Users\gitan\Desktop\Python Practice\UAS - DTU\arrows.png")

width,heigth = 640,480
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3,width)
cap.set(4,heigth)
b = 0
while True:
    suc, img = cap.read()
    
    
    hsvimg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #Identifying the red parts in an image
    #Lower Red - The start of HSV wheel
    lower1 = np.array([0, 100, 20])
    upper1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsvimg,lower1,upper1)
    #Upper Red - The end of HSV Wheel
    lower2 = np.array([160,100,20])
    upper2 = np.array([179,255,255])
    mask2 = cv2.inRange(hsvimg,lower2,upper2)
    mask = mask1 + mask2
    rdimg = cv2.bitwise_and(img,img, mask=mask)
    cv2.imshow("Output", rdimg)

    rdimg_grey = cv2.cvtColor(rdimg, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Output Grey", rdimg_grey)

    crnr = cv2.goodFeaturesToTrack(rdimg_grey, 5, 0.5, 10)
    print(crnr)
    try:

        corners = np.int0(crnr)
        for corner in corners:
            x,y = corner.ravel()
            cv2.circle(img, (x,y), 5, (0,255,0), -1)
        for i in corners[0]:
            a1 = i[0]
            b1 = i[1]
        for i in corners[1]:
            a2 = i[0]
            b2 = i[1]
        for i in corners[2]:
            a3 = i[0]
            b3 = i[1]
        for i in corners[3]:
            a4 = i[0]
            b4 = i[1]
        for i in corners[4]:
            a5 = i[0]
            b5 = i[1]
        
        am = a1+a2+a3+a4+a5
        bm = b1 + b2+ b3 + b4 + b5
        am /= 5
        bm /= 5
        print(am,bm)
        contours, hier = cv2.findContours(rdimg_grey, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours=sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True)
        
    #### DRAW A CIRCLE ARROUND THE ARROW TO FIND THE ANGLE OF THE ARROW
        for c in contours:
            # find minimum area
            x,y,w,h = cv2.boundingRect(c)
            (x,y),radius = cv2.minEnclosingCircle(c)
            center = (int(x),int(y))
            radius = int(radius)
            cv2.circle(img,center,radius,(0,255,0),2)
            cv2.circle(img,center,2,(0,255,0),2)
            cv2.circle(img,(int(am),int(bm)),2,(0,255,0),2)
        cv2.line(img,center,(int(am),int(bm)),(255,0,0),1)
        cv2.line(img,center,(int(radius+x),int(y)),(255,0,0),1)
        #Findind the tan of the angle to determine the angle of arrow
        atan=math.atan2(int(bm)-int(y),int(am)-int(x))
        angle=math.degrees(atan)
        angle = angle - 90
        #printing the arrow
        cv2.putText(img,str(angle),(10,85),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0))
        print ('angle=', angle)
    except:
        pass
    cv2.imshow("Output",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()