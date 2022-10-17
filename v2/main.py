import websockets
import asyncio
from pyngrok import ngrok
from skyfield.api import load

SERVER = '127.0.0.1'
PORT = 8000
SLEEP_TIME = 10
PLANET_SOURCE = 'earth'
PLANET_DESTINATION = 'moon'


def calc_radecdist(plnt_dst, plnt_src):
    t = load.timescale().now()
    moon, earth = load.planets[plnt_dst], load.planets[plnt_src]
    obsrvr = earth.at(t).observe(moon)
    ra, dec, dist = obsrvr.radec()
    return ra, dec


async def echo(websocket):
    while True:
        ra, dec = calc_radecdist(PLANET_DESTINATION, PLANET_SOURCE)
        msg = f'RA: {ra}; DEC: {dec}'
        await websocket.send(msg)
        print(msg)
        await asyncio.sleep(SLEEP_TIME)


def main():
    load.planets = load('de421.bsp')
    ngrok_conn = ngrok.connect(PORT, bind_tls=True)
    ngrok_url = ngrok_conn.public_url
    ra, dec = calc_radecdist(PLANET_DESTINATION, PLANET_SOURCE)
    msg = f'RA: {ra}; DEC: {dec}'
    print(msg)
    print(ngrok_url)
    websockets_serve = websockets.serve(echo, SERVER, PORT)
    asyncio.get_event_loop().run_until_complete(websockets_serve)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
