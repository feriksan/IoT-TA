from src.ObjectTracking.getMasking import getMasking
import asyncio
from websocket import Websocket

# from src.TcpClient import tcpClient

# firebase = FirebaseConnect()
# firebase.addSensor(1)
# firebase.readData()
# firebase.deleteSensorData(0)
# cap =  cv2.VideoCapture(0)

# Control Program
startWebsocket = Websocket()
beginWebsocket = startWebsocket.main()
asyncio.run(beginWebsocket())
# getMask = getMasking()
# getMask.startVideo()