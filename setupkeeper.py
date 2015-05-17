__author__ = 'zeferino'
import pickle

class setupkeeper:
    def __init__(self):
        self.fileobject = open("setup.conf", 'r')
        #self.cycles = pickle.load(self.fileobject)
        #self.sizes = pickle.load(self.fileobject)
        self.schedule = pickle.load(self.fileobject)
        self.thresholds = pickle.load(self.fileobject)
        self.plants = pickle.load(self.fileobject)
        self.gpscoordinates = pickle.load(self.fileobject)
        self.fileobject.close()
        self.read = True

    def getConf(self):
        self.fileobject = open("setup.conf", 'r')
        #self.cycles = pickle.load(self.fileobject)
        #self.sizes = pickle.load(self.fileobject)
        self.schedule = pickle.load(self.fileobject)
        self.thresholds = pickle.load(self.fileobject)
        self.plants = pickle.load(self.fileobject)
        self.gpscoordinates = pickle.load(self.fileobject)
        self.fileobject.close()
        self.read = True

    def updateConf(self):
        self.fileobject = open("setup.conf", 'wb')
        #pickle.dump(self.cycles, self.fileobject)
        #pickle.dump(self.sizes, self.fileobject)
        pickle.dump(self.schedule, self.fileobject)
        pickle.dump(self.thresholds, self.fileobject)
        pickle.dump(self.plants, self.fileobject)
        pickle.dump(self.gpscoordinates, self.fileobject)
        self.fileobject.close()
        self.read = False

    def isread(self):
        return self.read