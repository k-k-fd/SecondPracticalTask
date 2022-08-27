import websockets
import asyncio
from datetime import datetime
from pyngrok import ngrok


async def handler(websocket):
    print("A client just connected")
    try:
        while True:
            await websocket.send(str(datetime.now()))
            print(str(datetime.now()))
            await asyncio.sleep(2)
    except websockets.exceptions.ConnectionClosed:
        print("A client just disconnected")


if __name__ == "__main__":
    http_tunnel = ngrok.connect(8080, bind_tls=True)
    print("testing url is: ",http_tunnel.public_url)
    PORT = 8080
    start_server = websockets.serve(handler, "localhost", PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

