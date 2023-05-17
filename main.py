from src.ObjectTracking.getMasking import getMasking

# from src.TcpClient import tcpClient

# firebase = FirebaseConnect()
# firebase.addSensor(1)
# firebase.readData()
# firebase.deleteSensorData(0)
# cap =  cv2.VideoCapture(0)

# Control Program

getMask = getMasking()
getMask.startVideo()