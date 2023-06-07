import cv2, base64
import numpy as np
# from Firebase.firebaseConnect import FirebaseConnect
import time
import atexit
import math
from dotenv import load_dotenv
import models.maskingModel as dataMasking
import models.houghCircleModel as dataHough
import os

load_dotenv()

x = 0
y = 0

class getMasking:
    img_count = 0
    def __init__(self):
        print("Masuk")

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

    async def videoTracking(self, cap, websocket):
        _, frame = cap.read()
        await websocket.send("Connected")
        # Gaussian Blur
        Gaussian = cv2.GaussianBlur(frame, (7, 7), 0)

        hsv = cv2.cvtColor(Gaussian, cv2.COLOR_BGR2HSV)
        CAMERAHEIGHT = dataHough.CAMERA_HEIGHT
        BALL_DIAMETER = dataHough.BALL_DIAMETER
        UPPER_HUE = dataMasking.upperHue
        UPPER_SATURATION = dataMasking.upperSaturation
        UPPER_VALUE = dataMasking.upperValue
        LOWER_HUE = dataMasking.lowerHue
        LOWER_SATURATION = dataMasking.lowerSaturation
        LOWER_VALUE = dataMasking.lowerValue
        FOCAL_LENGHT = dataHough.FOCAL_LENGHT
        # print("CAMERA HEIGHT: " + CAMERAHEIGHT)
        # print("BALL DIAMETER: " + BALL_DIAMETER)
        # print("UPPER HUE: " + UPPER_HUE)
        # print("LOWER HUE: " + LOWER_HUE)
        # print("UPPER SATURATION: " + UPPER_SATURATION)
        # print("UPPER VALUE: " + UPPER_VALUE)
        # print("LOWER SATURATION: " + LOWER_SATURATION)
        # print("LOWER VALUE: " + LOWER_VALUE)
        # print("FOCAL LENGHT: " + FOCAL_LENGHT)
        print("Camera Height")
        print(CAMERAHEIGHT)
        print("Ball Diameter")
        print(BALL_DIAMETER)
        
        F = 45.78947368421053
        FinMM = 12.393640349315788
        fx2 = 1178.473863782612
        fx = 943.8170126557516
        fy = 899.3625747289594
        cx = 485.1822284643787
        cy = 273.7921446374951

        cameraHeight = int(CAMERAHEIGHT)
        objectDiameter = int(BALL_DIAMETER)


        # lower_blue = np.array([0, 0, 0])
        # upper_blue = np.array([255, 255, 255])

        # lower_red = np.array([0, 19, 43])
        # upper_red = np.array([26, 255, 152])

        # lower_blue = np.array([0, 67, 27])
        # upper_blue = np.array([71, 245, 255])

        lower_hsv = np.array([int(LOWER_HUE), int(LOWER_SATURATION), int(LOWER_VALUE)])
        upper_hsv = np.array([int(UPPER_HUE), int(UPPER_SATURATION), int(UPPER_VALUE)])
        
        mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
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
        try:
            circles = cv2.HoughCircles(blur_image,cv2.HOUGH_GRADIENT,1.1,w,
                            param1=100,param2=40,minRadius=30,maxRadius=177)
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
                        print("Parameter")
                        print(objectDiameter)
                        print(FinMM)
                        print(diameterInMM)
                        if(waterHeight > (cameraHeight-10) * 0.8):
                            waterStatus = "Siaga 1"
                        elif(waterHeight <= (cameraHeight-10) * 0.8 and waterHeight >= (cameraHeight-10) * 0.7):
                            waterStatus = "Siaga 2"
                        elif(waterHeight <= (cameraHeight-10) * 0.7 and waterHeight >= (cameraHeight-10) * 0.5):
                            waterStatus = "Siaga 3"
                        elif(waterHeight <= (cameraHeight-10) * 0.5):
                            waterStatus = "Aman"
                        print("JARAK", D)
                        print("Siaga 1", (cameraHeight-10) * 0.8)
                        print("Siaga 2", (cameraHeight-10) * 0.8, " - ", (cameraHeight-10) * 0.7)
                        print("Siaga 3", (cameraHeight-10) * 0.7, " - ", (cameraHeight-10) * 0.5)
                        print("Aman", (cameraHeight-10) * 0.5)
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

    async def startVideo(self,websocket, firebase):
        cap =  cv2.VideoCapture(0)
        width = 640
        height = 480
        self.firebase = firebase
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        # self.createWindows()
        # self.firebase.loadConfig()
        self.firebase.listenData()
        while True:
            await self.videoTracking(cap, websocket)
            key = cv2.waitKey(1)
            if key == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
        self.firebase.stopListening()
    
    def exit_handler(self):
    # do this stuff when the script exits
        return
