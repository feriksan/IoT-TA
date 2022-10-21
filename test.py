import cv2
import numpy as np
import matplotlib.image as mpimg
import urllib.request

def nothing(x):
    pass

# cap =  cv2.VideoCapture(0)
# prepare object points
nx = 8
ny = 6
url = 'http://192.168.174.209/capture'

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.


img_count = 0
while True:
    img_resp=urllib.request.urlopen(url)
    imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
    frame=cv2.imdecode(imgnp,-1)
    # _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)
    if ret == True:
        # objpoints.append(objp)
        # corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        # imgpoints.append(corners)
        # Draw and display the corners
        cv2.imwrite("foundImage/chessboard%d.png"%(img_count),frame)
        cv2.drawChessboardCorners(frame, (nx, ny), corners, ret)
        cv2.imwrite("calibratedImage/chessboard%d.png"%(img_count),frame)
        img_count+=1
        # ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        # print(mtx)
        # cv2.imshow("mask", frame)
    cv2.imshow("mask", gray)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
# cap.release()
cv2.destroyAllWindows()