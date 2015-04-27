__author__ = 'zeferino'

from datetime import datetime, timedelta, date
import time
from setupkeeper import setupkeeper
from forecast import forecast
from humiditySensor import humiditySensor


conf = setupkeeper()
humidity = humiditySensor()
rain_check = False #signal to check rain in that day
watering_action = False #signal to perform watering action
watering_postpone = False #signal that means we have to water some plants but the last time we try to do it, we can't for some reasons
deltatime = timedelta()
rain_check_time = datetime.combine(date.today(), time(23, 59))

def checkTimeToNextAction(raincheck, wateringaction, wateringpostpone):
    today = datetime.today()
    delta = rain_check_time - today
    raincheck = True
    wateringaction = False
    wateringpostpone = False
    i = 0
    while i < len(conf.plants):
        auxDelta = conf.plants[i].nextWateringTime() - today
        if auxDelta < delta and auxDelta > timedelta(0):
            delta = auxDelta
            wateringaction = True
            raincheck = False
            wateringpostpone = False
        auxDelta = conf.plants[i].getWateringTime() - today
        if conf.plants[i].getPostpone() and auxDelta <= delta:
            delta = auxDelta
            wateringpostpone = True
            raincheck = False
            wateringaction = False
        i += 1
    return delta

while 1:
    actualdate = datetime.today()
    conf.getConf()
    if rain_check:
        #get rain and update lastwatered time on plants if they need
        rain_check_time += timedelta(1)
        todayforecast = forecast(conf.gpscoordinates[0], conf.gpscoordinates[1])
        todayforecast.getCurrentWeather()
        rain_today = int(todayforecast.forecastJson['current_observation']['precip_today_metric'])
        i = 0
        while i < len(conf.plants):
            if conf.plants[i].size == 'small':
                if rain_today > conf.thresholds["smallthreshold"]:
                    conf.plants[i].watered()
                    conf.plants[i].setPostpone(False)
            elif conf.plants[i].size == 'medium':
                if rain_today > conf.thresholds["mediumthreshold"]:
                    conf.plants[i].watered()
                    conf.plants[i].setPostpone(False)
            elif conf.plants[i].size == 'large':
                if rain_today > conf.thresholds["largethreshold"]:
                    conf.plants[i].watered()
                    conf.plants[i].setPostpone(False)
            i += 1
        conf.updateConf()
        deltatime = checkTimeToNextAction(rain_check, watering_action, watering_postpone)
        time.sleep(deltatime.total_seconds())
    elif watering_postpone:
        #some plants have deferred watering actions

    elif watering_action:
        #perform watering actions


