import serial

__author__ = 'zeferino'
class Electrovalve:
    def __init__(self):
        self.value = 0
        self.quality = -1  # -1 valor invalido / 0 valor viejo / 1 valor bueno
        self.arduino = serial.Serial('/dev/tty.usbmodem621', 115200, timeout= 1.0)
#'''/dev/ttyACM0'''
    def getstate(self, addr):
        if addr < 1 or addr > 4:
            self.quality = self.quality if self.quality != 1 else 0
        else:
            self.arduino.write("EG" + str(addr) + "\n")
            s = self.arduino.readline()
            if s !="Recibido\n":
                self.quality = self.quality if self.quality != 1 else 0
            else:
                s = self.arduino.readline()
                sresult = s[0: len(s) - 1]
                self.value = int(sresult)
        return self.value, self.quality

    def openvalve(self, addr):
        if addr < 1 or addr > 4:
            self.quality = self.quality if self.quality != 1 else 0
        else:
            self.arduino.write("EO" + str(addr) + "\n")
            s = self.arduino.readline()
            if s !="Recibido\n":
                self.quality = self.quality if self.quality != 1 else 0
            else:
                s = self.arduino.readline()
                sresult = s[0: len(s) - 1]
                self.value = int(sresult)
        return self.value, self.quality

    def closevalve(self, addr):
        if addr < 1 or addr > 4:
            self.quality = self.quality if self.quality != 1 else 0
        else:
            self.arduino.write("EC" + str(addr) + "\n")
            s = self.arduino.readline()
            if s !="Recibido\n":
                self.quality = self.quality if self.quality != 1 else 0
            else:
                s = self.arduino.readline()
                sresult = s[0: len(s) - 1]
                self.value = int(sresult)
        return self.value, self.quality