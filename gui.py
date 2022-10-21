import cv2
import sys
import argparse
from collections import deque
from imutils.video import VideoStream
import time
import glob
import imutils
import threading
import numpy as np
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication, QPushButton, QProgressBar
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

class GetChessboard(QThread):
    changePixmap = pyqtSignal(QImage)
    changelabel = pyqtSignal(float)
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.stopStream = False
        self.window = parent

        self._lock = threading.Lock()
        self.running = False

    def stop(self):
        self.running = False
        self.stopStream = True
        print('received stop signal from window.')
        with self._lock:
            self._do_before_done()

    def _do_work(self):
        nx = 8
        ny = 6
        objp = np.zeros((6*7,3), np.float32)
        objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
        img_count = 0

        while True:
            frame = vs.read()
            frame = frame[1] if args.get("video", False) else frame
            if frame is None:
                break

            frame = imutils.resize(frame, width=600)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)
            if ret == True:
                cv2.imwrite("foundImage/chessboard%d.png"%(img_count),frame)
                cv2.drawChessboardCorners(frame, (nx, ny), corners, ret)
                cv2.imwrite("calibratedImage/chessboard%d.png"%(img_count),frame)
                img_count+=1
                self.changelabel.emit(img_count)
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(1000, 1000, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)
            if self.stopStream:
                break

    def _do_before_done(self):
        print('waiting 3 seconds before thread done..')
        for i in range(3, 0, -1):
            print('{0} seconds left...'.format(i))
            self.sleep(1)
        print('ok, thread done.')

    def run(self):
        self.running = True
        while self.running:
            with self._lock:
                self._do_work()

class CallibrateCamera(QThread):
    changelabel = pyqtSignal(float)
    changeMatrix = pyqtSignal(float, float, float, float)
    changePixmap = pyqtSignal(QImage)
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.window = parent

        self._lock = threading.Lock()
        self.running = False

    def stop(self):
        self.running = False
        print('received stop signal from window.')
        with self._lock:
            self._do_before_done()

    def _do_work(self):
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((6*7,3), np.float32)
        objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.
        progress = 0
        progress_total = 0

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
            progress+=1
            progress_total = (progress / len(images)) * 100
            if(progress_total == 100):
                self.running = False
            self.changelabel.emit(progress_total)
            img = cv2.imread(fname)
            rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(1000, 1000, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (7,6), None)
            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
                imgpoints.append(corners)
                ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
                fx.append(mtx[0][0])
                fy.append(mtx[1][1])
                cx.append(mtx[0][2])
                cy.append(mtx[1][2])
        fx_avr = np.average(fx)
        fy_avr = np.average(fy)
        cx_avr = np.average(cx)
        cy_avr = np.average(cy)
        self.changeMatrix.emit(fx_avr, fy_avr, cx_avr, cy_avr)

    def _do_before_done(self):
        print('waiting 3 seconds before thread done..')
        for i in range(3, 0, -1):
            print('{0} seconds left...'.format(i))
            self.sleep(1)
        print('ok, thread done.')

    def run(self):
        self.running = True
        while self.running:
            with self._lock:
                self._do_work()

class MotionTracking(QThread):
    changePixmap = pyqtSignal(QImage)
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.stopStream = False
        self.window = parent

        self._lock = threading.Lock()
        self.running = False

    def stop(self):
        self.running = False
        self.stopStream = True
        print('received stop signal from window.')
        with self._lock:
            self._do_before_done()

    def _do_work(self):
        print('thread is running...')
        fx = 943.8170126557516
        fy = 899.3625747289594
        cx = 485.1822284643787
        cy = 273.7921446374951
        pts = deque(maxlen=args["buffer"])
        while True:
            frame = vs.read()
            frame = frame[1] if args.get("video", False) else frame
            if frame is None:
                break

            # l_h = cv2.getTrackbarPos("L - H", "TrackBars")
            # l_s = cv2.getTrackbarPos("L - S", "TrackBars")
            # l_v = cv2.getTrackbarPos("L - V", "TrackBars")
            # u_h = cv2.getTrackbarPos("U - H", "TrackBars")
            # u_s = cv2.getTrackbarPos("U - S", "TrackBars")
            # u_v = cv2.getTrackbarPos("U - V", "TrackBars")

            # lower_treshold = np.array([l_h, l_s, l_v])
            # upper_treshold = np.array([u_h, u_s, u_v])
            greenLower = (0, 24, 23)
            greenUpper = (22, 255, 255)

            frame = imutils.resize(frame, width=600)
            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, greenLower, greenUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            center = None
            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                if radius > 10:
                    Z = (fx * 0.02)/(radius)
                    X = ((int(x) - cx) * Z)/fx
                    Y = ((int(y) - cy) * Z)/fy
                    cv2.circle(frame, (int(x), int(y)), int(radius),
                        (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
            pts.appendleft(center)

            for i in range(1, len(pts)):
                if pts[i - 1] is None or pts[i] is None:
                    continue
                thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(1000, 1000, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)
            if self.stopStream:
                break

    def _do_before_done(self):
        print('waiting 3 seconds before thread done..')
        for i in range(3, 0, -1):
            print('{0} seconds left...'.format(i))
            self.sleep(1)
        print('ok, thread done.')

    def run(self):
        self.running = True
        while self.running:
            with self._lock:
                self._do_work()

class App(QWidget):
    def __init__(self, app):
        super().__init__()
        self.title = 'PyQt5 Video'
        self.left = 500
        self.top = 100
        self.width = 100
        self.height = 100
        self.initUI(app)

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))
    
    @pyqtSlot()
    def resetProgress(self):
        self.pbar.setValue(0)

    @pyqtSlot(float)
    def setLabel(self, imgFound):
        if(imgFound == 100):
            self.th.stop()
        # self.label2.setText("Image Found: %i" % imgFound)
        self.pbar.setValue(imgFound)

    @pyqtSlot(float, float, float, float)
    def setMatrix(self, fx, fy, cx, cy):
        self.label2.setText("Fx: %f" % fx)
        self.label3.setText("Fy: %f" % fy)
        self.label4.setText("Cx: %f" % cx)
        self.label5.setText("Cy: %f" % cy)

    @pyqtSlot()
    def startCalibrate(self):
        self.label2.setText("Fx: 0")
        self.label3.setText("Fy: 0")
        self.label4.setText("Cx: 0")
        self.label5.setText("Cy: 0")

    def initUI(self, app):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(1000, 1000)
        # create a label
        self.label = QLabel(self)
        self.label.move(0, -125)
        self.label.resize(1000, 1000)

        self.label2 = QLabel(self)
        self.label2.setObjectName("label2")
        self.label2.setText("Fx: --------------------------")
        self.label2.move(200,860)

        self.label3 = QLabel(self)
        self.label3.setObjectName("label3")
        self.label3.setText("Fy: --------------------------")
        self.label3.move(330,860)

        self.label4 = QLabel(self)
        self.label4.setObjectName("label4")
        self.label4.setText("Cx: --------------------------")
        self.label4.move(460,860)

        self.label5 = QLabel(self)
        self.label5.setObjectName("label5")
        self.label5.setText("Cy: --------------------------")
        self.label5.move(590,860)

        callibrateBtn = QPushButton('Get Image For Callibrate', self)
        callibrateBtn.setToolTip('Get Image For Callibration')
        callibrateBtn.move(200,800)

        stopCallibrateBtn = QPushButton('Stop', self)
        stopCallibrateBtn.setToolTip('Stop')
        stopCallibrateBtn.move(200,825)

        motionTrackingBtn = QPushButton('Motion Tracking', self)
        motionTrackingBtn.setToolTip('Start Motion Tracking')
        motionTrackingBtn.move(600,800)

        stopMotionTrackingBtn = QPushButton('Stop Motion Tracking', self)
        stopMotionTrackingBtn.setToolTip('Stop Motion Tracking')
        stopMotionTrackingBtn.move(600,825)

        callibrateCameraBtn = QPushButton('Calibrate Camera', self)
        callibrateCameraBtn.setToolTip('Calibrate Camera')
        callibrateCameraBtn.move(400,800)

        stopCallibrateBtn = QPushButton('Stop', self)
        stopCallibrateBtn.setToolTip('Stop')
        stopCallibrateBtn.move(400,825)

        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)
        self.pbar.resize(600, 20)
        self.pbar.move(200,900)

        self.th = GetChessboard(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.changelabel.connect(self.setLabel)
        callibrateBtn.clicked.connect(self.th.start)
        stopCallibrateBtn.clicked.connect(self.th.stop)

        self.th3 = CallibrateCamera(self)
        self.th3.changelabel.connect(self.setLabel)
        self.th3.changeMatrix.connect(self.setMatrix)
        self.th3.changePixmap.connect(self.setImage)
        callibrateCameraBtn.clicked.connect(self.startCalibrate)
        callibrateCameraBtn.clicked.connect(self.resetProgress)
        callibrateCameraBtn.clicked.connect(self.th3.start)
        stopCallibrateBtn.clicked.connect(self.th3.stop)

        th2 = MotionTracking(self)
        th2.changePixmap.connect(self.setImage)
        motionTrackingBtn.clicked.connect(self.resetProgress)
        motionTrackingBtn.clicked.connect(th2.start)
        stopMotionTrackingBtn.clicked.connect(th2.stop)

if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
        help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64,
        help="max buffer size")
    args = vars(ap.parse_args())
    if not args.get("video", False):
        vs = VideoStream(src=0).start()
    # otherwise, grab a reference to the video file
    else:
        vs = cv2.VideoCapture(args["video"])
    app = QApplication(sys.argv)
    window = App(app)
    window.show()
    # ex = App()
    sys.exit(app.exec_())