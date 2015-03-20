'''import pywapi
import xmltodict
import urllib2

def gps():
    print "Escribe latitud apreta enter:"
    datos = raw_input();
    print "Escribe longitud apreta enter:"
    datos2 = raw_input();
    tupla_gps = [datos, datos2]
    #tupla_gps = [53.244921, -2.479539]
    return tupla_gps


datos_gps = gps()

url = "http://maps.googleapis.com/maps/api/geocode/xml?latlng=%s,%s&sensor=true" % (datos_gps[0], datos_gps[1])
response = urllib2.urlopen(url)
xml = response.read()
xmlparsed = xmltodict.parse(xml)
#xmlparsed["GeocodeResponse"]["result"][0]["address_component"][3]["long_name"]#acceso a nombre de ciudad
city = xmlparsed["GeocodeResponse"]["result"][0]["address_component"][3]["long_name"]
location_id = pywapi.get_location_ids(city)
weather = pywapi.get_weather_from_yahoo(location_id, units = 'metric')
'''
import pyowm
import urllib2
import json
import requests

def gps():
    #print "Escribe latitud apreta enter:"
    #datos = raw_input();
    #print "Escribe longitud apreta enter:"
    #datos2 = raw_input();
    tupla_gps = {'lat': "41.22", 'lon': "1.53"}
    #tupla_gps = [53.244921, -2.479539]
    return tupla_gps

def weather_coord(coords):
    urlweather = "http://api.openweathermap.org/data/2.5/weather"
    r = requests.get(urlweather, params=coords)
    print(r.json())


def forecast_coord(coords):
    urlforecast = "http://api.openweathermap.org/data/2.5/forecast"
    r = requests.get(urlforecast, params=coords)
    print(r.json())


datos_gps = gps()
weather_coord(datos_gps)
forecast_coord(datos_gps)



'''pensamiento, ciclame, margaritas

pensamiento riego cada 8 o 10 dias invierno, en verano 2 o 3 veces por semana (l, x, v)
margarita 8 o 10 dias invierno, verano 2 o 3 veces por semana
ciclame invierno cada 10 dias, verano 2 o 3 veces'''



