__author__ = 'zeferino'

from datetime import datetime, timedelta, date
import time
from setupkeeper import setupkeeper
from forecast import forecast
from humiditySensor import humiditySensor
from temperatureSensor import temperatureSensor
from Electrovalve import Electrovalve
from Levelsensor import Levelsensor
import thread


conf = setupkeeper()
temp = temperatureSensor()
valves = Electrovalve()
level = Levelsensor()
temperaturethreshold = 3
levelthreshold = 400
summer = [4, 9]
timewhilewatering = 60
rain_check = False #signal to check rain in that day
watering_action = False #signal to perform watering action
watering_postpone = False #signal that means we have to water some plants but the last time we try to do it, we can't for some reasons
plant_postpone = 0
deltatime = timedelta()
rain_check_time = datetime.combine(date.today(), time(23, 59))

def checkTimeToNextAction(raincheck, wateringaction, wateringpostpone, plantpostpone):
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
        auxDelta = conf.plants[i].getWateringTime() + conf.plants[i].getLastWatering() - today
        if conf.plants[i].getPostpone() and auxDelta <= delta:
            delta = auxDelta
            plantpostpone = i
            wateringpostpone = True
            raincheck = False
            wateringaction = False
        i += 1
    return delta

def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def stopwatering(plant):
    time.sleep(360)
    if level.getvalue() > levelthreshold:
        valves.openvalve(7)
    else:
        valves.closevalve(7)
    time.sleep(240)
    valves.closevalve(plant+4)
    return

def watering(plant):
    if level.getvalue() > levelthreshold:
        valves.openvalve(7)
    else:
        valves.closevalve(7)
    valves.openvalve(plant+4)
    thread.start_new_thread(stopwatering, plant)

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
        deltatime = checkTimeToNextAction(rain_check, watering_action, watering_postpone, plant_postpone)
        time.sleep(deltatime.total_seconds())
    elif watering_postpone:
        #some plants have deferred watering actions
        humiditythreshold = 400 #esto hay que mirarlo
        if conf.plants[plant_postpone].gethumidity() > humiditythreshold:
            conf.plants[plant_postpone].watered()
            watering_postpone = False
        else:
            if temp.getvalue() > temperaturethreshold:
                    today = datetime.today()
                    if time_in_range(summer[0], summer[1], today.month):
                        if time_in_range(conf.schedule['summer'][0], conf.schedule['summer'][1], today.time()):
                            watering_postpone = False
                            watering(plant_postpone)
                        else:
                            addtime = datetime.combine(date.today(), conf.schedule['summer'][0]) - today
                            conf.plants[plant_postpone].setWateringTime(conf.plants[plant_postpone].getWateringTime()+ addtime)
                    else:
                        if time_in_range(conf.schedule['winter'][0], conf.schedule['winter'][1], today.time()):
                            watering_postpone = False
                            watering(plant_postpone)
                        else:
                            addtime = datetime.combine(date.today(), conf.schedule['winter'][0]) - today
                            conf.plants[plant_postpone].setWateringTime(conf.plants[plant_postpone].getWateringTime()+ addtime)
            else:
                conf.plants[plant_postpone].setWateringTime(conf.plants[plant_postpone].getWateringTime()+ timedelta(1))
    elif watering_action:
        #perform watering actions


