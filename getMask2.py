import cv2
import numpy as np
from collections import deque
from imutils.video import VideoStream
import argparse
import imutils
import time

def nothing(x):
    pass

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

cv2.namedWindow("TrackBars")

cv2.createTrackbar("L - H", "TrackBars", 0, 179, nothing)
cv2.createTrackbar("L - S", "TrackBars", 0, 255, nothing)
cv2.createTrackbar("L - V", "TrackBars", 0, 255, nothing)
cv2.createTrackbar("U - H", "TrackBars", 179, 179, nothing)
cv2.createTrackbar("U - S", "TrackBars", 255, 255, nothing)
cv2.createTrackbar("U - V", "TrackBars", 255, 255, nothing)

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (0, 24, 23)
greenUpper = (22, 255, 255)

fx = 943.8170126557516
fy = 899.3625747289594
cx = 485.1822284643787
cy = 273.7921446374951

pts = deque(maxlen=args["buffer"])
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start()
# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])
# allow the camera or video file to warm up
time.sleep(2.0)
# keep looping
while True:
    # grab the current frame
    frame = vs.read()
    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break
    # resize the frame, blur it, and convert it to the HSV
    # color space

    l_h = cv2.getTrackbarPos("L - H", "TrackBars")
    l_s = cv2.getTrackbarPos("L - S", "TrackBars")
    l_v = cv2.getTrackbarPos("L - V", "TrackBars")
    u_h = cv2.getTrackbarPos("U - H", "TrackBars")
    u_s = cv2.getTrackbarPos("U - S", "TrackBars")
    u_v = cv2.getTrackbarPos("U - V", "TrackBars")

    lower_treshold = np.array([0, 24, 23])
    upper_treshold = np.array([22, 255, 255])

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, lower_treshold, upper_treshold)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
        if radius > 10:
            Z = (fx * 0.02)/(radius)
            X = ((int(x) - cx) * Z)/fx
            Y = ((int(y) - cy) * Z)/fy
            # print("Z Pos: ", Z - (0.4815299109073973))
            print("X Pos: ", X - (-0.13274344879587063))
            # print("Y Pos: ", Y - (-0.014344847542938004))

            if(Z - (0.4815299109073973) < -0.02):
                print("Kurang Mundur")
            
            if(Z - (0.4815299109073973) > 0.02):
                print("Kurang Maju")

            # file = open("data.txt", "a")
            # content2 = str(X)
            # content3 = str(0)
            # content = str(Z)
            # file.write(content2 + "," + content3 + "," + content + "\n")
            # file.close()
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
    # update the points queue
    pts.appendleft(center)

    # loop over the set of tracked points
    for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()
# otherwise, release the camera
else:
	vs.release()
# close all windows
cv2.destroyAllWindows()