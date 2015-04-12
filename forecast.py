__author__ = 'zeferino'

import requests
import json


class forecast:
    def __init__(self, lat, lon):
        self.apiId = '3be88c886dd44892'
        self.url = 'http://api.wunderground.com/api/{0}/{1}/{2}/q/{3},{4}.json'
        self.lat = lat
        self.lon = lon
        self.forecastJson = ''
        self.historyJson = ''

    def getCurrentWeather(self):
        urlForecast = self.url.format(self.apiId, 'conditions', 'lang:SP', self.lat, self.lon)
        r = requests.get(urlForecast)
        self.forecastJson = r.json()
        return self.forecastJson

    def getHistory(self, date):
        historyday = 'history_' + date
        urlHistory = self.url.format(self.apiId, historyday, 'lang:SP', self.lat, self.lon)
        r = requests.get(urlHistory)
        self.historyJson = r.json()
        return self.historyJson

