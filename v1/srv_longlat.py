import websockets
import asyncio
import math
from datetime import datetime
from pyngrok import ngrok


SERVER = '127.0.0.1'
PORT = 8000
SLEEP_TIME = 10


def frac(x):
    return x - math.floor(x)


def calc_t(y):
    """
    param y: current year
    return: number of Julian centuries between the epoch and 2000 January 1
    """
    return y - 2000 / 100


def calc_lon_lat(t):
    """
    param t: number of Julian centuries between the epoch and 2000 January 1
    """
    pi = math.pi
    pi2 = 2.0 * pi
    arcs = 3600.0 * 180.0 / pi
    # Mean elements of lunar orbit
    l_0 = frac(0.606433 + 1336.855225 * t)  # mean longitude [rev]
    al = pi2 * frac(0.374897 + 1325.552410 * t)  # Moon’s mean anomaly
    ls = pi2 * frac(0.993133 + 99.997361 * t)  # Sun’s mean anomaly
    d = pi2 * frac(0.827361 + 1236.853086 * t)  # Diff.long.Moon - Sun
    f = pi2 * frac(0.259086 + 1342.227825 * t)  # Dist. from ascending node
    # Perturbations in longitude and latitude
    dl = 22640 * math.sin(al) - 4586 * math.sin(al - 2 * d) + 2370 * \
        math.sin(2 * d) + 769 * math.sin(2 * al) - 668 * math.sin(ls) - 412 * \
        math.sin(2 * f) - 212 * math.sin(2 * al - 2 * d) - 206 * \
        math.sin(al + ls - 2 * d) + 192 * math.sin(al + 2 * d) - 165 * \
        math.sin(ls - 2 * d) - 125 * math.sin(d) - 110 * \
        math.sin(al + ls) + 148 * math.sin(al - ls) - 55 * \
        math.sin(2 * f - 2 * d)
    s = f + (dl + 412 * math.sin(2 * f) + 541 * math.sin(ls)) / arcs
    h = f - 2 * d
    n = -526 * math.sin(h) + 44 * math.sin(al + h) - 31 * \
        math.sin(-al + h) - 23 * math.sin(ls + h) + 11 * \
        math.sin(-ls + h) - 25 * math.sin(-2 * al + f) + 21 * \
        math.sin(-al + f)
    # Ecliptic longitude and latitude
    l_moon = pi2 * frac(l_0 + dl / 1296.0e3)  # [rad]
    b_moon = (18520.0 * math.sin(s) + n) / arcs  # [rad]
    return l_moon, b_moon


def msg_create_ip_time():
    now = datetime.now()
    now_str = now.strftime("%Y/%m/%d %H:%M:%S")
    return f'The server is on. IP:{SERVER} PORT:{PORT} DATE/TIME:{now_str}'


def msg_create():
    t = calc_t(datetime.now().year)
    longitude, latitude = calc_lon_lat(t)[0], calc_lon_lat(t)[1]
    return f'longitude: {longitude}; latitude: {latitude}'


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
