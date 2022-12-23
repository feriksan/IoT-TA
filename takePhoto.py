import cv2

videoCaptureObject = cv2.VideoCapture(0)
videoCaptureObject.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
videoCaptureObject.set(cv2.CAP_PROP_FPS, 25)
while(True):
    ret,frame = videoCaptureObject.read()
    cv2.imshow('Capturing Video',frame)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        videoCaptureObject.release()
        cv2.destroyAllWindows()
    elif(cv2.waitKey(1) & 0xFF == ord('p')):
        cv2.imwrite("sample.jpg",frame)