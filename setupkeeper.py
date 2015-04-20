__author__ = 'zeferino'
import pickle

class setupkeeper:
    def __init__(self):
        self.fileobject = open("setup.txt", 'r')
        self.cycles = pickle.load(self.fileobject)
        self.schedule = pickle.load(self.fileobject)
        self.thresholds = pickle.load(self.fileobject)
        self.sizes = pickle.load(self.fileobject)
        self.plants = pickle.load(self.fileobject)
        self.fileobject.close()

    def getConf(self):
        self.fileobject = open("setup.txt", 'r')
        self.cycles = pickle.load(self.fileobject)
        self.schedule = pickle.load(self.fileobject)
        self.thresholds = pickle.load(self.fileobject)
        self.sizes = pickle.load(self.fileobject)
        self.plants = pickle.load(self.fileobject)
        self.fileobject.close()

    def updateConf(self):
        self.fileobject = open("setup.txt", 'wb')
        pickle.dump(self.cycles, self.fileobject)
        pickle.dump(self.schedule, self.fileobject)
        pickle.dump(self.thresholds, self.fileobject)
        pickle.dump(self.sizes, self.fileobject)
        pickle.dump(self.plants, self.fileobject)
        self.fileobject.close()