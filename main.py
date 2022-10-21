from src.ObjectTracking.getMasking import getMasking
from Firebase.firebaseConnect import FirebaseConnect
import cv2
# from src.TcpClient import tcpClient

# firebase = FirebaseConnect()
# firebase.addSensor(1)
# firebase.readData()
# firebase.deleteSensorData(0)
# cap =  cv2.VideoCapture(0)
getMask = getMasking()
video = getMask.startVideo()
video()