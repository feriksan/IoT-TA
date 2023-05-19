import asyncio
from websockets.server import serve
import cv2, base64

async def echo(websocket):
    print("MASOK")
    async for message in websocket:
        print("Masok")
        await websocket.send(message)

async def transmit(websocket):
    print("Client Connected !")
    try :
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            _, frame = cap.read()
            
            encoded = cv2.imencode('.jpg', frame)[1]

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

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())