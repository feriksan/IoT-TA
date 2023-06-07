import asyncio
from websockets.server import serve
from src.config.maskingConfig.masking import Masking
from src.config.measurementConfig.measurement import Measurement
from src.ObjectTracking.getMasking import getMasking
from multiprocessing import active_children
from Firebase.firebaseConnect import FirebaseConnect

class Websocket:
    async def startWebsocket(self, websocket):
        async for message in websocket:
            if(message == "1"):
                startMasking = Masking()
                await startMasking.main(websocket, self.firebase)
            elif(message == "2"):
                startMeasurement = Measurement()
                await startMeasurement.main(websocket, self.firebase)
            elif(message == "3"):
                getMask = getMasking()
                getMask.startVideo(self.firebase)
            elif(message == "4"):
                active = active_children()
                print(active)

    async def main(self):
        print("Masuk main")
        url1 = "192.168.1.21"
        url2 = "localhost"
        self.firebase = FirebaseConnect()
        async with serve(self.startWebsocket, url1, 8765):
            await asyncio.Future()
