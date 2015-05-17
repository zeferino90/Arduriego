import serial

__author__ = 'zeferino'
class Levelsensor:
    def __init__(self):
        self.value = 0
        self.quality = -1 #-1 valor invalido / 0 valor viejo / 1 valor bueno
        self.arduino = serial.Serial('/dev/ttyACM0', 115200, timeout= 1.0)

    def getvalue(self):
        self.arduino.flushInput()
        self.arduino.flushOutput()
        self.arduino.write("N" + "\n")
        s = self.arduino.readline()
        if s !="Recibido\n":
            self.quality = self.quality if self.quality != 1 else 0
            self.value = -1
        else:
            s = self.arduino.readline()
            sresult=s[0: len(s) - 1]
            self.value=float(sresult)
        return (self.value, self.quality)