import numpy as np
import cv2 as cv
import glob
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

fx = []
fy = []
cx = []
cy = []

fx_avr = 0
fy_avr = 0
cx_avr = 0
cy_avr = 0

images = glob.glob('foundImage/*.png')
for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (7,6), None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        fx.append(mtx[0][0])
        fy.append(mtx[1][1])
        cx.append(mtx[0][2])
        cy.append(mtx[1][2])
        # Draw and display the corners
        # cv.drawChessboardCorners(img, (7,6), corners2, ret)
        # cv.imshow('img', img)
        # cv.waitKey(500)
fx_avr = np.average(fx)
fy_avr = np.average(fy)
cx_avr = np.average(cx)
cy_avr = np.average(cy)
print("Fx: ", fx_avr)
print("Fy: ", fy_avr)
print("Cx: ", cx_avr)
print("Cy: ", cy_avr)

cv.destroyAllWindows()