__author__ = 'zeferino'

from datetime import datetime, timedelta
import time
import setupkeeper
import forecast


conf = setupkeeper()
rain_check = False #signal to check rain in that day
watering_action = False #signal to perform watering action
watering_postpone = False #signal that means we have to water some plants but the last time we try to do it, we can't for some reasons
deltatime = timedelta()
onedaydelta = timedelta(1)

def checkTimeToNextAction():
    delta = timedelta()

    return delta

while 1:
    actualdate = datetime.today()
    conf.getConf()
    if rain_check:
        #get rain and update lastwatered time on plants if they need
        todayforecast = forecast(conf.gpscoordinates[0], conf.gpscoordinates[1])
        todayforecast.getCurrentWeather()
        rain_today = int(todayforecast.forecastJson['current_observation']['precip_today_metric'])
        i = 0
        while i < len(conf.plants):
            if conf.plants[i].size == 'small':
                if rain_today > conf.thresholds["smallthreshold"]:
                    conf.plants[i].watered()
            elif conf.plants[i].size == 'medium':
                if rain_today > conf.thresholds["mediumthreshold"]:
                    conf.plants[i].watered()
            elif conf.plants[i].size == 'large':
                if rain_today > conf.thresholds["largethreshold"]:
                    conf.plants[i].watered()
            i+=1
        conf.updateConf()
        deltatime = checkTimeToNextAction()
        if onedaydelta > deltatime:
            deltatime = onedaydelta
        time.sleep(deltatime.total_seconds())
    elif watering_action:
        #perform watering actions
    elif watering_postpone:
        #some plants have deferred watering actions

