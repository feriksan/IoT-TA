import cv2

nx = 8
ny = 6

img_count = 0

videoCaptureObject = cv2.VideoCapture(0)
while(True):
    ret,frame = videoCaptureObject.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("frame", frame)
    ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)
    if ret == True:
        # objpoints.append(objp)
        # corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        # imgpoints.append(corners)
        # Draw and display the corners
        cv2.imwrite("foundImage3/chessboard%d.png"%(img_count),frame)
        cv2.drawChessboardCorners(frame, (nx, ny), corners, ret)
        cv2.imwrite("calibratedImage2/chessboard%d.png"%(img_count),frame)
        img_count+=1
        print(img_count)
        # ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        # print(mtx)
        # cv2.imshow("mask", frame)
    cv2.imshow("mask", gray)

    if(cv2.waitKey(1) & 0xFF == ord('q')):
        videoCaptureObject.release()
        cv2.destroyAllWindows()
    elif(cv2.waitKey(1) & 0xFF == ord('p')):
        cv2.imwrite("sample.jpg",frame)