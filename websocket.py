import asyncio
from websockets.server import serve
from src.config.maskingConfig.masking import Masking
from src.config.measurementConfig.measurement import Measurement
from src.ObjectTracking.getMasking import getMasking
from multiprocessing import active_children

class Websocket:
    async def startWebsocket(self, websocket):
        async for message in websocket:
            if(message == "1"):
                startMasking = Masking()
                await startMasking.main(websocket)
            elif(message == "2"):
                startMeasurement = Measurement()
                await startMeasurement.main(websocket)
            elif(message == "3"):
                getMask = getMasking()
                getMask.startVideo()
            elif(message == "4"):
                active = active_children()
                print(active)

    async def main(self):
        print("Masuk main")
        url1 = "192.168.1.21"
        url2 = "localhost"
        async with serve(self.startWebsocket, url2, 8765):
            await asyncio.Future()
