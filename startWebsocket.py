import asyncio
from websocket import Websocket
from multiprocessing import Process

startWebsocket = Websocket()
asyncio.run(startWebsocket.main())