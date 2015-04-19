from datetime import datetime

__author__ = 'zeferino'

class plant:
    def __init__(self, name, cycle, siz):
        self.id = 0 #aixo es comprovara mirant el arxiu
        self.name = name
        self.cycle = cycle
        self.siz = siz
        self.lastw = datetime.today()

    def getName(self):
        return self.name

    def getCycle(self):
        return self.cycle

    def getPotSize(self):
        return self.siz

    def getLastWatering(self):
        return self.lastw

    def setName(self, newname):
        self.name = newname

    def setCycle(self, newcycle):
        self.cycl = newcycle

    def setPotSize(self, newsize):
        self.siz = newsize

    def watered(self):
        self.lastw = datetime.today()