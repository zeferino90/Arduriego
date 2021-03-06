import serial

__author__ = 'zeferino'


class Electrovalve:
    def __init__(self):
        self.value = 0
        self.quality = -1  # -1 valor invalido / 0 valor viejo / 1 valor bueno
        self.arduino = serial.Serial('/dev/ttyACM0', 115200, timeout= 1.0)
#'''/dev/tty.usbmodem621'''

    def RepresentsInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def getstate(self, addr):
        self.arduino.flushInput()
        self.arduino.flushOutput()
        if addr < 1 or addr > 4:
            print "Invalid ddres \n"
            self.quality = self.quality if self.quality != 1 else 0
        else:
            print "Address {}".format(addr)
            self.arduino.write("EG" + str(addr) + "\n")
            s = self.arduino.readline()
            if s !="Recibido\n":
                print "Arduino not response\n"
                self.quality = self.quality if self.quality != 1 else 0
                self.value = -1
            else:
                s = self.arduino.readline()
                print "Valor de arduino {}".format(s)
                sresult = s[0: len(s) - 1]
                print "Valor tratado {}".format(sresult)
                if not self.RepresentsInt(sresult):
                    self.value = -1
                else:
                    self.value = int(sresult)
        return self.value, self.quality

    def openvalve(self, addr):
        self.arduino.flushInput()
        self.arduino.flushOutput()
        if addr < 1 or addr > 4:
            print "Invalid ddres \n"
            self.quality = self.quality if self.quality != 1 else 0
        else:
            print "Address {}".format(addr)
            self.arduino.write("EO" + str(addr) + "\n")
            s = self.arduino.readline()
            if s !="Recibido\n":
                print "Arduino not response\n"
                self.quality = self.quality if self.quality != 1 else 0
                self.value = -1
            else:
                s = self.arduino.readline()
                print "Valor de arduino {}".format(s)
                sresult = s[0: len(s) - 1]
                print "Valor tratado {}".format(sresult)
                if not self.RepresentsInt(sresult):
                    self.value = -1
                else:
                    self.value = int(sresult)
        return self.value, self.quality

    def closevalve(self, addr):
        self.arduino.flushInput()
        self.arduino.flushOutput()
        if addr < 1 or addr > 4:
            print "Invalid ddres \n"
            self.quality = self.quality if self.quality != 1 else 0
        else:
            print "Address {}".format(addr)
            self.arduino.write("EC" + str(addr) + "\n")
            s = self.arduino.readline()
            if s !="Recibido\n":
                print "Arduino not response\n"
                self.quality = self.quality if self.quality != 1 else 0
                self.value = -1
            else:
                s = self.arduino.readline()
                print "Valor de arduino {}".format(s)
                sresult = s[0: len(s) - 1]
                print "Valor tratado {}".format(sresult)
                if not self.RepresentsInt(sresult):
                    self.value = -1
                else:
                    self.value = int(sresult)
        return self.value, self.quality

