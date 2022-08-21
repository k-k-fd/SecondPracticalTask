import socket
import time
from datetime import datetime
from pyngrok import ngrok


# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = '127.0.0.1'
PORT = 3000
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def start():
    server.listen()
    print(f'Server has started on {SERVER}')
    while True:
        now = datetime.now()
        now_str = now.strftime("%Y/%m/%d %H:%M:%S")
        print(f'The server is on. IP:{SERVER} PORT:{PORT} DATE/TIME:{now_str} ...')
        time.sleep(10)


start()
