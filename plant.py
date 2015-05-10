from datetime import datetime
from datetime import timedelta
from humiditySensor import humiditySensor

__author__ = 'zeferino'
#moi es mas feo que pegar a un padre
class plant:
    def __init__(self, name, cycle, siz, wtime, addres, sensorhumidity):
        self.name = name
        self.cycle = cycle #timedelta
        self.siz = siz
        self.wateringTime = wtime #deltatime for postpone
        self.postpone = False
        self.lastw = None
        self.humidityaddres = addres
        self.lastw = datetime.today()

    def __str__(self):
        result = "name: " + self.name + "\n"
        result += "cycle: " + str(self.cycle) + "\n"
        result += "size: " + str(self.siz) + "\n"
        result += "watering time: " + str(self.wateringTime) + "\n"
        result += "postpone: " + str(self.postpone) + "\n"
        result += "last watering: " + str(self.lastw) + "\n"
        result += "humidity sensor address: " + str(self.humidityaddres) + "\n"
        return result

    def getName(self):
        return self.name

    def getCycle(self):
        return self.cycle

    def getPotSize(self):
        return self.siz

    def getLastWatering(self):
        return self.lastw

    def getWateringTime(self):
        return self.wateringTime

    def getPostpone(self):
        return self.postpone

    def getHumidity(self):
        return humiditySensor().getvalue(self.humidityaddres)

    def setName(self, newname):
        self.name = newname

    def setCycle(self, newcycle):
        self.cycle = newcycle

    def setPotSize(self, newsize):
        self.siz = newsize

    def setWateringTime(self, newWTime):
        self.wateringTime = newWTime

    def setPostpone(self, newPostpone):
        self.postpone = newPostpone

    def watered(self):
        self.lastw = datetime.today()

    def nextWateringTime(self):
        return self.lastw + self.cycle