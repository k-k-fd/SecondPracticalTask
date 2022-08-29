import websockets
import asyncio
from datetime import datetime
from pyngrok import ngrok
import ephem

SERVER = '127.0.0.1'
PORT = 8000
SLEEP_TIME = 10
OBSRVR_LONG = '79.3832'
OBSRVR_LAT = '43.6532'
OBSRVR_DATE = datetime.now()


def calc_radec():
    obsrvr = ephem.Observer()
    obsrvr.lon, obsrvr.lat = OBSRVR_LONG, OBSRVR_LAT
    obsrvr.date = OBSRVR_DATE
    moon = ephem.Moon()
    moon.compute(obsrvr)
    return moon.ra, moon.dec


def msg_create_ip_time():
    now = datetime.now()
    now_str = now.strftime("%Y/%m/%d %H:%M:%S")
    return f'The server is on. IP:{SERVER} PORT:{PORT} DATE/TIME:{now_str}'


def msg_create():
    ra, dec = calc_radec()[0], calc_radec()[1]
    return f'RA: {ra}; DEC: {dec}'


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
