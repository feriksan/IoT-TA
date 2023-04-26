import cv2
import numpy as np
from Firebase.firebaseConnect import FirebaseConnect
import time
import atexit
import math
from dotenv import load_dotenv
import os

load_dotenv()

x = 0
y = 0

class getMasking:
    img_count = 0
    def __init__(self):
        self.firebase = FirebaseConnect()

    def nothing(self, x):
        pass

    def createWindows(self):
        cv2.namedWindow("TrackBars")
        cv2.createTrackbar("L - H", "TrackBars", 0, 255, self.nothing)
        cv2.createTrackbar("L - S", "TrackBars", 0, 255, self.nothing)
        cv2.createTrackbar("L - V", "TrackBars", 0, 255, self.nothing)
        cv2.createTrackbar("U - H", "TrackBars", 255, 255, self.nothing)
        cv2.createTrackbar("U - S", "TrackBars", 255, 255, self.nothing)
        cv2.createTrackbar("U - V", "TrackBars", 255, 255, self.nothing)

        greenLower = (0, 24, 23)
        greenUpper = (22, 255, 255)

    def videoTracking(self, cap):
        _, frame = cap.read()
        # Gaussian Blur
        Gaussian = cv2.GaussianBlur(frame, (7, 7), 0)

        hsv = cv2.cvtColor(Gaussian, cv2.COLOR_BGR2HSV)
        CAMERAHEIGHT = os.getenv('CAMERA_HEIGHT')
        OBJECT_DIAMETER = os.getenv('OBJECT_DIAMETER')
        
        F = 45.78947368421053
        FinMM = 12.393640349315788
        fx2 = 1178.473863782612
        fx = 943.8170126557516
        fy = 899.3625747289594
        cx = 485.1822284643787
        cy = 273.7921446374951

        cameraHeight = int(CAMERAHEIGHT)
        objectDiameter = int(OBJECT_DIAMETER)


        lower_blue = np.array([0, 0, 0])
        upper_blue = np.array([255, 255, 255])


        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #looping for contours
        for c in contours:
            if cv2.contourArea(c) < 500:
                continue
                
            #get bounding box from countour
            (x, y, w, h) = cv2.boundingRect(c)
            
            #draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        result = cv2.bitwise_and(frame, frame, mask=mask)
        # Convert to greyscale
        img_gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
        blur_image = cv2.GaussianBlur(img_gray, (3, 3), 1)

        # Apply Hough transform to greyscale image
        circles = cv2.HoughCircles(blur_image,cv2.HOUGH_GRADIENT,1,w,
                            param1=90,param2=50,minRadius=0,maxRadius=0)
        try:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(result,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(result,(i[0],i[1]),2,(0,0,255),3)
                diameterList = []
                diameterMean = 0
                # print(i[0])
                if(self.img_count < 16):
                    diameterList.append(i[2])
                    if(self.img_count == 15):
                        diameterMean = np.average(diameterList)
                        diameterInMM = diameterMean * 0.2645833333
                        D = (objectDiameter*FinMM)/diameterInMM
                        waterHeight = cameraHeight-D
                        if(waterHeight < 0):
                            waterHeight = 0
                        # print(D)
                        # perpindahan = i[0] - 320
                        # print("perpindahan", perpindahan)
                        # perpindahanMM = perpindahan * 0.2645833333
                        # print("perpindahan riil", perpindahanMM)
                        # tan = perpindahanMM/FinMM
                        # print("Jarak Didapat", D)
                        # sudutSebenarnya = 90 - tan - 40
                        # print(sudutSebenarnya)
                        # angle1 = math.radians(sudutSebenarnya)
                        # jarakSebenarnya = (D+(3.8/2)) * math.sin(angle1)
                        # print(jarakSebenarnya)
                        # print(jarakSebenarnya)
                        waterStatus = ""
                        if(waterHeight > (cameraHeight-10) * 0.8):
                            waterStatus = "Siaga 1"
                        elif(waterHeight <= (cameraHeight-10) * 0.8 and waterHeight >= (cameraHeight-10) * 0.7):
                            waterStatus = "Siaga 2"
                        elif(waterHeight <= (cameraHeight-10) * 0.7 and waterHeight >= (cameraHeight-10) * 0.5):
                            waterStatus = "Siaga 3"
                        elif(waterHeight <= (cameraHeight-10) * 0.5):
                            waterStatus = "Aman"
                        print("JARAK", D)
                        self.firebase.updateWaterHeight(waterHeight, D, waterStatus)
                        # file.write(str(D) + "," + str(diameterMean) + "," + str(waterHeight) +  "," +  contentTrue + "," +  cameraDistanceTrue + "\n")
                        # file.close()
                else:
                    self.img_count = 0
                    diameterList = []
            self.img_count+=1
            #     Z_median = []
            #     Z = (fx2 * objectDiameter)/(i[2])
            #     # F = (i[2] * 60)/38
            #     # print(F)
            #     D = (38*F)/i[2]
            #     # print(D)
            #     if(self.img_count < 16):
            #         Z_median.append(Z)
            #         if(self.img_count == 15):
            #             Z = np.average(Z_median)
            #             waterHeight = cameraHeight-Z
            #             print(D)
            #             waterStatus = "Safe" if Z > cameraHeight else "Not Safe"
            #             self.firebase.updateWaterHeight(waterHeight, cameraHeight, Z, objectDiameter, waterStatus)
            #     else:
            #         self.img_count = 0
            #         Z_median = []
            # self.img_count+=1
            
        except Exception as e:
            print("no circle")
        # Draw the circles

        # cv2.imshow("mask", mask)
       	cv2.imshow("result", result)

    def startVideo(self):
        cap =  cv2.VideoCapture(0)
        # self.createWindows()
        self.firebase.loadConfig()
        while True:
            self.videoTracking(cap)
            key = cv2.waitKey(1)
            if key == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
    
    def exit_handler(self):
    # do this stuff when the script exits
        return
