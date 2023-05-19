import asyncio
from websockets.server import serve
import cv2, base64
import numpy as np
import os

async def transmit(websocket):
    print("Client Connected !")
    try :
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            _, frame = cap.read()

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            UPPER_HUE = os.getenv('UPPER_HUE')
            UPPER_SATURATION = os.getenv('UPPER_SATURATION')
            UPPER_VALUE = os.getenv('UPPER_VALUE')
            LOWER_HUE = os.getenv('LOWER_HUE')
            LOWER_SATURATION = os.getenv('LOWER_SATURATION')
            LOWER_VALUE = os.getenv('LOWER_VALUE')

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
    except:
        print("Someting went Wrong !")
        cap.release()

async def sendData(websocket, data):
    await websocket.send(data)

async def main():
    async with serve(transmit, "192.168.1.22", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())