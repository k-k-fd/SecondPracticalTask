import websockets
import asyncio
from datetime import datetime
from pyngrok import ngrok

SERVER = '127.0.0.1'
PORT = 8000
SLEEP_TIME = 3

def calc_ra():
    return None

def msg_create(ngrok_link):
    now = datetime.now()
    now_str = now.strftime("%Y/%m/%d %H:%M:%S")
    return f'The server is on. IP:{SERVER} PORT:{PORT} DATE/TIME:{now_str} \n PUBLIC URL:{ngrok_link}'

def msg_create_no_link():
    now = datetime.now()
    now_str = now.strftime("%Y/%m/%d %H:%M:%S")
    return f'The server is on. IP:{SERVER} PORT:{PORT} DATE/TIME:{now_str}'
async def echo(websocket):
    while True:
        await websocket.send(msg_create_no_link())
        print(msg_create_no_link())
        await asyncio.sleep(SLEEP_TIME)
def main():
    ngrok_conn = ngrok.connect(PORT, bind_tls=True)
    ngrok_url = ngrok_conn.public_url
    print(msg_create(ngrok_url))
    websockets_serve = websockets.serve(echo, SERVER, PORT)
    asyncio.get_event_loop().run_until_complete(websockets_serve)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()




'''import websockets
import asyncio
from pyngrok import ngrok
from datetime import datetime

SERVER = '127.0.0.1'
PORT = 8000
SLEEP_TIME = 3

# def msg_create(ngrok_link):
#     now = datetime.now()
#     now_str = now.strftime("%Y/%m/%d %H:%M:%S")
#     return f'The server is on. IP:{SERVER} PORT:{PORT} DATE/TIME:{now_str} \n PUBLIC URL:{ngrok_link}'

async def echo(websocket):
    while True:
        await websocket.send("hi")
        print("123")
        await asyncio.sleep(2)

def main():
        ngrok_conn = ngrok.connect(PORT, bind_tls=True)
        ngrok_url = ngrok_conn.public_url
        websockets_serve = websockets.serve(echo, SERVER, PORT)
        asyncio.get_event_loop().run_until_complete(websockets_serve)
        asyncio.get_event_loop().run_forever()
        # await asyncio.Future()  # run forever
        # while True:
        #     print(msg_create(ngrok_url))
        #     time.sleep(SLEEP_TIME)
'''
