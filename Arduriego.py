__author__ = 'zeferino'

from datetime import *
import time as times
from setupkeeper import setupkeeper
from forecast import forecast
from temperatureSensor import temperatureSensor
from Electrovalve import Electrovalve
from Levelsensor import Levelsensor
import thread
import setup


conf = setupkeeper()

temp = temperatureSensor()
valves = Electrovalve()
level = Levelsensor()
temperaturethreshold = 3
levelthreshold = 400
humiditythreshold = 500
summer = [4, 9]
timewhilewatering = 60
rain_check = False #signal to check rain in that day
watering_action = False #signal to perform watering action
watering_postpone = False #signal that means we have to water some plants but the last time we try to do it, we can't for some reasons
plant_postpone = 0
plant_to_water = 0
deltatime = timedelta()
rain_check_time = datetime.combine(date.today(), time(23, 59))

def writeLog(log):
    f = open("logsArduriego.txt", "a")
    f.write(log + "\n")
    f.close()

def checkTimeToNextAction():
    writeLog("Check Time to Next Action")
    today = datetime.today()
    delta = rain_check_time - today
    global rain_check
    rain_check = True
    global watering_action
    watering_action = False
    global watering_postpone
    watering_postpone = False
    global plant_to_water
    global plant_postpone
    i = 0
    while i < len(conf.plants):
        auxDelta = conf.plants[i].nextWateringTime() - today
        writeLog("Watering AuxDelta{}: ".format(i) + str(auxDelta))
        if auxDelta < delta:
            delta = auxDelta
            watering_action = True
            plant_to_water = i
            rain_check = False
            watering_postpone = False
        auxDelta = conf.plants[i].getWateringTime() + conf.plants[i].getLastWatering() - today
        writeLog("postpone AuxDelta{}: ".format(i) + str(auxDelta))
        if conf.plants[i].getPostpone() and auxDelta <= delta:
            plant_postpone = i
            watering_postpone = True
            rain_check = False
            watering_action = False
        i += 1
    if auxDelta < timedelta(0):
        delta = timedelta(0)
    else:
        delta = auxDelta
    writeLog("  Result:")
    writeLog("    wateringaction " + str(watering_action))
    writeLog("    planttowater " + str(plant_to_water))
    writeLog("    raincheck " + str(rain_check))
    writeLog("    wateringpostpone " + str(watering_postpone))
    writeLog("    plantpostpone " + str(plant_postpone))
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


checkTimeToNextAction()
while 1:
    actualdate = datetime.today()
    writeLog("Actualdate: " + str(actualdate))
    writeLog("  rain_check : " + str(rain_check))
    writeLog("  rain-check_time: " + str(rain_check_time))
    writeLog("  watering_action: " + str(watering_action))
    writeLog("  plan_to_water: " + str(plant_to_water))
    writeLog("  watering_postpone: " + str(watering_postpone))
    writeLog("  plant_postpone: " + str(plant_postpone))
    if not conf.isread():
        conf.getConf()
        writeLog("Conf update")
    if rain_check:
        writeLog("Rain check action")
        #get rain and update lastwatered time on plants if they need
        rain_check_time += timedelta(1)
        todayforecast = forecast(conf.gpscoordinates[0], conf.gpscoordinates[1])
        todayforecast.getCurrentWeather()
        rain_today = int(todayforecast.forecastJson['current_observation']['precip_today_metric'])
        writeLog("Rain today: " + str(rain_today))
        i = 0
        while i < len(conf.plants):
            if conf.plants[i].getPotSize() == 'small':
                writeLog("Small threshold: " + str(conf.thresholds['smallthreshold']))
                if rain_today > conf.thresholds['smallthreshold']:
                    conf.plants[i].watered()
                    conf.plants[i].setPostpone(False)
            elif conf.plants[i].getPotSize() == 'medium':
                if rain_today > conf.thresholds['mediumthreshold']:
                    conf.plants[i].watered()
                    conf.plants[i].setPostpone(False)
            elif conf.plants[i].getPotSize() == 'large':
                if rain_today > conf.thresholds['largethreshold']:
                    conf.plants[i].watered()
                    conf.plants[i].setPostpone(False)
            i += 1
        deltatime = checkTimeToNextAction()
        conf.updateConf()
        writeLog("Sleeeping while " + str(deltatime.total_seconds()))
        times.sleep(int(deltatime.total_seconds()))
    elif watering_postpone:
        writeLog("Watering postpone action")
        #some plants have deferred watering actions
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
                            conf.plants[plant_postpone].setPostpone(False)
                        else:
                            addtime = datetime.combine(date.today(), conf.schedule['summer'][0]) - today
                            conf.plants[plant_postpone].setWateringTime(conf.plants[plant_postpone].getWateringTime()+ addtime)
                    else:
                        if time_in_range(conf.schedule['winter'][0], conf.schedule['winter'][1], today.time()):
                            watering_postpone = False
                            watering(plant_postpone)
                            conf.plants[plant_postpone].setPostpone(False)
                        else:
                            addtime = datetime.combine(date.today(), conf.schedule['winter'][0]) - today
                            conf.plants[plant_postpone].setWateringTime(conf.plants[plant_postpone].getWateringTime()+ addtime)
            else:
                conf.plants[plant_postpone].setWateringTime(conf.plants[plant_postpone].getWateringTime()+ timedelta(1))
        deltatime = checkTimeToNextAction()
        conf.updateConf()
        writeLog("Sleeeping while " + str(deltatime.total_seconds()))

        times.sleep(int(deltatime.total_seconds()))

    elif watering_action:
        writeLog("Watering action")
        #perform watering actions
        if conf.plants[plant_to_water].getHumidity() > humiditythreshold:
            conf.plants[plant_to_water].watered()
            watering_action = False
        else:
            if temp.getvalue() > temperaturethreshold:
                    today = datetime.today()
                    if time_in_range(summer[0], summer[1], today.month):
                        if time_in_range(conf.schedule['summer'][0], conf.schedule['summer'][1], today.time()):
                            watering_action = False
                            watering(plant_to_water)
                            conf.plants[plant_to_water].watered()
                        else:
                            addtime = datetime.combine(date.today(), conf.schedule['summer'][0]) - today
                            conf.plants[plant_to_water].setWateringTime(addtime)
                            conf.plants[plant_to_water].setPostpone(True)
                    else:
                        if time_in_range(conf.schedule['winter'][0], conf.schedule['winter'][1], today.time()):
                            watering_action = False
                            watering(plant_to_water)
                            conf.plants[plant_to_water].watered()
                        else:
                            addtime = datetime.combine(date.today(), conf.schedule['winter'][0]) - today
                            conf.plants[plant_to_water].setWateringTime(addtime)
                            conf.plants[plant_to_water].setPostpone(True)
            else:
                conf.plants[plant_to_water].setWateringTime(timedelta(hours=1))
                conf.plants[plant_to_water].setPostpone(True)
        deltatime = checkTimeToNextAction()
        conf.updateConf()
        writeLog("Sleeeping while " + str(deltatime.total_seconds()))
        times.sleep(int(deltatime.total_seconds()))