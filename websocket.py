import asyncio
from websockets.server import serve
import cv2, base64
import numpy as np
import models.maskingModel as dataAAA
import os

class Websocket:
    async def transmit(self, websocket):
        print("Client Connected !")
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            _, frame = cap.read()

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            UPPER_HUE = 255
            UPPER_SATURATION = 255
            UPPER_VALUE = 255
            LOWER_HUE = 0
            LOWER_SATURATION = 0
            LOWER_VALUE = 0
            print("LOWER HUE DATA")
            print(dataAAA.lowerHue)
            lower_hsv = np.array([int(LOWER_HUE), int(LOWER_SATURATION), int(LOWER_VALUE)])
            upper_hsv = np.array([int(UPPER_HUE), int(UPPER_SATURATION), int(UPPER_VALUE)])
            
            mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            #looping for contours
            for c in contours:
                if cv2.contourArea(c) < 500:
                    continue
                    
                #get bounding box from countour
                (x, y, w, h) = cv2.boundingRect(c)
                
                #draw bounding box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            result = cv2.bitwise_and(frame, frame, mask=mask)
            encoded = cv2.imencode('.jpg', result)[1]

            data = str(base64.b64encode(encoded))
            data = data[2:len(data)-1]
            
            await websocket.send(data)
            
            # cv2.imshow("Transimission", frame)
            
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
        cap.release()

    async def sendData(self, websocket, data):
        await websocket.send(data)

    async def main(self):
        print("Masuk main")
        async with serve(self.transmit, "192.168.1.18", 8765):
            print("Websocket")
            await asyncio.Future()  # run forever
