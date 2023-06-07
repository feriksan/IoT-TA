import asyncio
from websocket import Websocket

startWebsocket = Websocket()
asyncio.run(startWebsocket.main())