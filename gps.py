import serial

__author__ = 'zeferino'
class gps:
    def __init__(self):
        self.lat = 0
        self.long = 0
        self.fix = False
        self.quality = -1 #-1 valor invalido / 0 valor viejo / 1 valor bueno
        self.arduino = serial.Serial('/dev/ttyACM0', 115200, timeout= 1.0)

    def getcoordinates(self):
        self.arduino.write("GC")
        s = self.arduino.readline()
        if s !="Recibido\n":
            self.quality = self.quality if self.quality != 1 else 0
        else:
            s = self.arduino.readline()
            sresult=s[0: len(s) - 1]
            sresults = sresult.split(" ")
            self.lat = sresults[0]
            self.long = sresults[1]
        return (self.lat, self.long, self.quality)

    def getfix(self):
        self.arduino.write("GF")
        s = self.arduino.readline()
        if s !="Recibido\n":
            self.quality = self.quality if self.quality != 1 else 0
        else:
            s = self.arduino.readline()
            sresult=s[0: len(s) - 1]
            if sresult == "False":
                self.fix = False
            else:
                self.fix = True
        return (self.fix, self.quality)
'''deberia poder pedir el estado del gps(si tiene senal o no) i pedir sus coordenadas'''