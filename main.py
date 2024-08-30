import os
import math
import urllib3


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)


def download_tile(zoom, x, y, directory):
    url = f'https://a.tile.openstreetmap.org/{zoom}/{x}/{y}.png'
    http = urllib3.PoolManager()
    response = http.request('GET', url)

    if not os.path.exists(f"{directory}/{zoom}/{x}/"):
        os.makedirs(f"{directory}/{zoom}/{x}/")

    with open(os.path.join(directory, f"{zoom}/{x}/{y}.png"), 'wb') as file:
        file.write(response.data)
        print(f"Downloaded tile {zoom}-{x}-{y}")


def download_scheme(lat_deg, lon_deg, delta_lat, delta_long, zoom_st, zoom_fn):
    for zoom in range(zoom_st, zoom_fn+1):
        xmin, ymax = deg2num(lat_deg-delta_lat, lon_deg-delta_lat, zoom)
        xmax, ymin = deg2num(lat_deg + delta_lat, lon_deg + delta_long, zoom)

        for x in range(xmin, xmax+1):
            for y in range(ymin, ymax+1):
                print(zoom, x, y)
                download_tile(zoom, x, y, directory)

def download_all(zoom):
    for zoom in range(0, zoom+1):
        xmax = 2**zoom
        ymax = 2**zoom

        for x in range(0, xmax):
            for y in range(0, ymax):
                print(zoom, x, y)
                download_tile(zoom, x, y, directory)


if __name__ == '__main__':
    directory = "tiles_moscow"

    if not os.path.exists(directory):
        os.makedirs(directory)
    # download_all(7)
    #москва 55 с.ш 37 з.д.
    download_scheme(55.75, 37.6, 3, 4, 13, 14)