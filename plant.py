from datetime import datetime
from datetime import timedelta

__author__ = 'zeferino'
#moi es mas feo que pegar a un padre
class plant:
    def __init__(self, name, cycle, siz, wtime):
        self.id = 0 #aixo es comprovara mirant el arxiu
        self.name = name
        self.cycle = cycle
        self.siz = siz
        self.wateringTime = wtime #timedelta
        self.postpone = False
        self.lastw = datetime.today()

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

    def setName(self, newname):
        self.name = newname

    def setCycle(self, newcycle):
        self.cycl = newcycle

    def setPotSize(self, newsize):
        self.siz = newsize

    def setWateringTime(self, newWTime):
        self.wateringTime = newWTime

    def setPostpone(self, newPostpone):
        self.postpone = newPostpone

    def watered(self):
        self.lastw = datetime.today()