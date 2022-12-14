import cv2
import numpy as np
import urllib.request

def nothing(x):
    pass

cap =  cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
url = 'http://192.168.174.209/capture'
cv2.namedWindow("TrackBars")

cv2.createTrackbar("L - H", "TrackBars", 0, 179, nothing)
cv2.createTrackbar("L - S", "TrackBars", 0, 255, nothing)
cv2.createTrackbar("L - V", "TrackBars", 0, 255, nothing)
cv2.createTrackbar("U - H", "TrackBars", 179, 179, nothing)
cv2.createTrackbar("U - S", "TrackBars", 255, 255, nothing)
cv2.createTrackbar("U - V", "TrackBars", 255, 255, nothing)

object_detector = cv2.createBackgroundSubtractorMOG2()
x_array = []
y_array = []
z_array = []
img_count = 0
while True:
    # img_resp=urllib.request.urlopen(url)
    # imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
    # frame2=cv2.imdecode(imgnp,-1)
    _, frame = cap.read()
    # Gaussian Blur
    Gaussian = cv2.GaussianBlur(frame, (7, 7), 0)

    hsv = cv2.cvtColor(Gaussian, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L - H", "TrackBars")
    l_s = cv2.getTrackbarPos("L - S", "TrackBars")
    l_v = cv2.getTrackbarPos("L - V", "TrackBars")
    u_h = cv2.getTrackbarPos("U - H", "TrackBars")
    u_s = cv2.getTrackbarPos("U - S", "TrackBars")
    u_v = cv2.getTrackbarPos("U - V", "TrackBars")
    
    fx = 943.8170126557516
    fy = 899.3625747289594
    cx = 485.1822284643787
    cy = 273.7921446374951

    # fx = 1210.0984606828474
    # fy = 1189.9836526890997
    # cx = 688.1041102116526
    # cy = 394.38596525781395

    lower_blue = np.array([l_h, l_s, l_v])
    upper_blue = np.array([u_h, u_s, u_v])

    #Blue mask
    # lower_blue = np.array([89, 154, 109])
    # upper_blue = np.array([97, 205, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # mask = object_detector.apply(Gaussian)
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
    # img = cv2.medianBlur(result,3)
    # img_copy = img.copy()
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
            Z_median = []
            Z = (fx * 0.02)/(i[2])
            X = ((i[0] - cx) * Z)/fx
            Y = ((i[1] - cy) * Z)/fy
            file = open("dataLinear.txt", "a")
            fileNoisy = open("dataLinearNoisy.txt", "a")
            # cv2.imwrite("blurImage/ball%d.png"%(img_count),frame)
            print("Ketinggian Air", 34 - Z*100)
            contentTrue = "60"
            if(img_count < 16):
                Z_median.append(Z)
                if(img_count == 15):
                    Z = np.average(Z_median)
                    content3 = str(Z*100)
                    # contentError = contentTrue - content3
                    file.write(content3 + "," + contentTrue + "\n")
                    file.close()
            else:
                img_count = 0
                Z_median = []
            # img_count+=1
            # content2 = str(X)
            # content = str(0)
            
            contentNoise = str(Z*100)
            fileNoisy.write(contentNoise + "," + contentTrue + "\n")
            fileNoisy.close()

            # x_array.append(X)
            # y_array.append(Y)
            # z_array.append(Z)

            focal_lenght = (i[2] * 30)/4
            distance = (4*420)/i[2]
            img_count+=1
            
    except:
        print("no circle")
    # Draw the circles


    # cv2.imshow("frame", frame)
    cv2.imshow("mask", frame)
    cv2.imshow("result", result)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.destroyAllWindows()