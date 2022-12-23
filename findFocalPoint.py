import cv2
import numpy as np

videoCaptureObject = cv2.VideoCapture(0)
img_count = 0
jarak_diuji = 60
diameter_objek = 38

while(True):
    ret,frame = videoCaptureObject.read()
    lower_blue = np.array([0, 0, 0])
    upper_blue = np.array([255, 255, 255])

    Gaussian = cv2.GaussianBlur(frame, (7, 7), 0)

    hsv = cv2.cvtColor(Gaussian, cv2.COLOR_BGR2HSV)
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
    img_gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
    blur_image = cv2.GaussianBlur(img_gray, (3, 3), 1)
    edges = cv2.Canny(img_gray,100,200)

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
            F = (i[2] * jarak_diuji)/diameter_objek
            F_Mean = []
            if(img_count < 16):
                F_Mean.append(F)
                if(img_count == 15):
                    F = np.average(F_Mean)
                    print(F)
            else:
                img_count = 0
                F_Mean = []

        img_count+=1
        
    except:
        print("no circle")
    # Draw the circles
    cv2.imshow("mask", result)
    cv2.imshow("Canny", edges)

    if(cv2.waitKey(1) & 0xFF == ord('q')):
        videoCaptureObject.release()
        cv2.destroyAllWindows()
    elif(cv2.waitKey(1) & 0xFF == ord('p')):
        cv2.imwrite("sample.jpg",frame)