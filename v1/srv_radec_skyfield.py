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
    return ra, dec, dist


def msg_create(planet_dst, planet_src):
    ra, dec, dist = calc_radecdist(planet_dst, planet_src)
    return f'RA: {ra}; DEC: {dec}'


async def echo(websocket):
    while True:
        await websocket.send(msg_create(PLANET_DESTINATION, PLANET_SOURCE))
        print(msg_create(PLANET_DESTINATION, PLANET_SOURCE))
        await asyncio.sleep(SLEEP_TIME)


def main():
    load.planets = load('de421.bsp')
    ngrok_conn = ngrok.connect(PORT, bind_tls=True)
    ngrok_url = ngrok_conn.public_url
    print(msg_create(PLANET_DESTINATION, PLANET_SOURCE))
    print(ngrok_url)
    websockets_serve = websockets.serve(echo, SERVER, PORT)
    asyncio.get_event_loop().run_until_complete(websockets_serve)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
