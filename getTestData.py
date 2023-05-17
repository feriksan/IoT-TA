import cv2
import numpy as np
import urllib.request

def nothing(x):
    pass

cap =  cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
# width = 1920
# height = 1080
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
url = 'http://192.168.174.209/capture'
cv2.namedWindow("TrackBars")

cv2.createTrackbar("L - H", "TrackBars", 0, 255, nothing)
cv2.createTrackbar("L - S", "TrackBars", 0, 255, nothing)
cv2.createTrackbar("L - V", "TrackBars", 0, 255, nothing)
cv2.createTrackbar("U - H", "TrackBars", 255, 255, nothing)
cv2.createTrackbar("U - S", "TrackBars", 255, 255, nothing)
cv2.createTrackbar("U - V", "TrackBars", 255, 255, nothing)

object_detector = cv2.createBackgroundSubtractorMOG2()
x_array = []
y_array = []
z_array = []
img_count = 0

while True:
    _, frame = cap.read()
    # Gaussian Blur
    cv2.imshow("result", frame)
    Gaussian = cv2.GaussianBlur(frame, (7, 7), 0)

    hsv = cv2.cvtColor(Gaussian, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L - H", "TrackBars")
    l_s = cv2.getTrackbarPos("L - S", "TrackBars")
    l_v = cv2.getTrackbarPos("L - V", "TrackBars")
    u_h = cv2.getTrackbarPos("U - H", "TrackBars")
    u_s = cv2.getTrackbarPos("U - S", "TrackBars")
    u_v = cv2.getTrackbarPos("U - V", "TrackBars")
    
    F = 45.78947368421053
    cameraHeight = 60
    objectDiameter = 0.038
    contentTrue = "1"
    cameraDistanceTrue = "59"


    # lower_blue = np.array([0, 67, 27])
    # upper_blue = np.array([71, 245, 255])

    lower_blue = np.array([58, 177, 41])
    upper_blue = np.array([163, 255, 155])

    lower_pink = np.array([126, 0, 26])
    upper_pink = np.array([255, 255, 255])

    lower_pink = np.array([0, 193, 95])
    upper_pink = np.array([19, 255, 255])

    lower_yellow = np.array([19, 133, 95])
    upper_yellow = np.array([90, 255, 255])

    lower_red = np.array([0, 19, 43])
    upper_red = np.array([26, 255, 152])

    lower_test = np.array([l_h, l_s, l_v])
    upper_test = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_test, upper_test)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #looping for contours
    for c in contours:
        if cv2.contourArea(c) < 500:
            continue
            
        #get bounding box from countour
        (x, y, w, h) = cv2.boundingRect(c)
        
        #draw bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    print(w)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    # Convert to greyscale
    img_gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
    blur_image = cv2.GaussianBlur(img_gray, (7, 7), 1)

    try:
        print(w)
            # Apply Hough transform to greyscale image
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
            # file = open("dataWithDiameter.txt", "a")
            if(img_count < 16):
                diameterList.append(i[2])
                if(img_count == 15):
                    diameterMean = np.average(diameterList)
                    D = (38*F)/diameterMean
                    waterHeight = cameraHeight-D
                    print(diameterMean)
                    # file.write(str(D) + "," + str(diameterMean) + "," + str(waterHeight) +  "," +  contentTrue + "," +  cameraDistanceTrue + "\n")
                    # file.close()
            else:
                img_count = 0
                diameterList = []
            img_count+=1

            # Z_median = []
            # Z = 0
            # D = (38*F)/i[2]
            # # print(D)
            # file = open("dataLinear2.txt", "a")
            # fileNoisy = open("dataLinearNoisy2.txt", "a")
            # if(img_count < 16):
            #     Z_median.append(Z)
            #     diameterMedian.append(i[2])
            #     if(img_count == 15):
            #         Z = np.average(Z_median)
            #         waterHeight = cameraHeight-Z
            #         content3 = str(waterHeight)
            #         print(cameraHeight-Z)
            #         file.write(content3 + "," + contentTrue + "\n")
            #         file.close()
            # else:
            #     img_count = 0
            #     Z_median = []
        
        # fileNoisy.write(str(D) + "," + contentTrue + "\n")
        # fileNoisy.close()
        
    except Exception as e:
        print("no circle")
    # Draw the circles
    # cv2.imshow("HSV", hsv)
    # cv2.imshow("mask", mask)
    cv2.imshow("result", frame)
    # cv2.imshow("Gray", img_gray)
    # cv2.imshow("Blur", blur_image)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.destroyAllWindows()