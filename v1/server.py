import websockets
import asyncio
from datetime import datetime
from pyngrok import ngrok

SERVER = '127.0.0.1'
PORT = 8000
SLEEP_TIME = 3


def calc_ra():
    return None


def calc_dec():
    return None


def msg_create():
    now = datetime.now()
    now_str = now.strftime("%Y/%m/%d %H:%M:%S")
    return f'The server is on. IP:{SERVER} PORT:{PORT} DATE/TIME:{now_str}'


async def echo(websocket):
    while True:
        await websocket.send(msg_create())
        print(msg_create())
        await asyncio.sleep(SLEEP_TIME)


def main():
    ngrok_conn = ngrok.connect(PORT, bind_tls=True)
    ngrok_url = ngrok_conn.public_url
    print(msg_create())
    print(ngrok_url)
    websockets_serve = websockets.serve(echo, SERVER, PORT)
    asyncio.get_event_loop().run_until_complete(websockets_serve)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
