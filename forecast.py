__author__ = 'zeferino'

import requests

class forecast:
    def __init__(self):
        self.apiId = '0322a8ae89b2d00a65ef04c33ac4a37d'
        self.params = {'lat': "0", 'lon': "0", 'APPID': self.apiId}
        self.urlForecast = "http://api.openweathermap.org/data/2.5/weather"
        self.urlHistorical = "http://api.openweathermap.org/data/2.5/history/city"
        self.forecastJson = " "
        self.historicalJson = " "

    def getCurrentWeather(self):
        r = requests.get(self.urlForecast, params=self.params)
        self.forecastJson = r.json()
        return self.forecastJson