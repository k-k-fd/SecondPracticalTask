import websockets
import asyncio
from datetime import datetime

SERVER = '127.0.0.1'
PORT = 8000
SLEEP_TIME = 10

now = datetime.now()
now_str = now.strftime("%Y/%m/%d %H:%M:%S")
msg = f'The server is on. IP:{SERVER} PORT:{PORT} DATE/TIME:{now_str} ...'

async def handler(websocket):
    while True:
        await websocket.send(msg)
        await asyncio.sleep(SLEEP_TIME)

start = websockets.serve(handler, SERVER, PORT)
asyncio.get_event_loop().run_until_complete(start)
asyncio.get_event_loop().run_forever()

