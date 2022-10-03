import urllib
import requests as R
import json as J

baseImageUrl = "https://maps.googleapis.com/maps/api/staticmap"
baseURL = "https://maps.googleapis.com/maps/api/geocode/json"
AUTH_KEY = ""

def getAuthKey():
    global AUTH_KEY
    with open('mapAuth', 'r') as file:
        AUTH_KEY = file.read()

def getStaticMapParameters(location, size='1024x768', style='roadmap', zoom=10):
    return {
        'location': location,
        'size': size,
        'style': style,
        'zoom': zoom,
        'key': AUTH_KEY
    }

def getStaticImage(location):
    parameters = getStaticMapParameters(address)
    parameters = urllib.parse.urlencode(parameters)

def getGeoParameters(address):
    return {
        'address': address,
        'key': AUTH_KEY
    }

def getLocation(address):
    parameters = getGeoParameters(address)
    parameters = urllib.parse.urlencode(parameters)
    page = R.get(f'{baseUrl}{parameters}')

def point2LatLong(lat, long, x, y, w, h, zoom=10):
    parallelMultiplier = math.cos(lat * math.pi / 180)
    degreesPerPixelX = 360 / math.pow(2, zoom + 8)
    degreesPerPixelY = 360 / math.pow(2, zoom + 8) * parallelMultiplier
    pointLat = lat - degreesPerPixelY * ( y - h / 2)
    pointLong = long + degreesPerPixelX * ( x  - w / 2)
    return (pointLat, pointLong

def getEdgeLatLong(lat, long, w, h):
    nw = point2LatLong(lat, long, 0, 0)
    ne = point2LatLong(lat, long, w, 0)    nw = point2LatLong(lat, long, 0, 0)    nw = point2LatLong(lat, long, 0, 0)
    sw = point2LatLong(lat, long, 0, h)
    se = point2LatLong(lat, long, w, h)
    return nw, ne, sw, se

def latLong2Point(lat, long, w, h):
    nw, ne, sw, se = getEdgeLatLong(lat, long, w, h)
    xDelta = ne-hw
    yDelta = sw-nw
    return int(w*(lat/xDelta)), int(h*(long/yDelta))
