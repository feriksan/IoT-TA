from src.ObjectTracking.getMasking import getMasking
import asyncio
# from websocket import Websocket
# from Firebase.firebaseConnect import FirebaseConnect

# from src.TcpClient import tcpClient

# firebase = FirebaseConnect()
# firebase.listenData()
# firebase.addSensor(1)
# firebase.readData()
# firebase.deleteSensorData(0)
# cap =  cv2.VideoCapture(0)

# Control Program
# getMask = getMasking()
# getMask.startVideo()

startWebsocket = Websocket()
asyncio.run(startWebsocket.main())