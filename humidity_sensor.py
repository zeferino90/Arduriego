import serial

__author__ = 'zeferino'
class humidity_sensor:
    def __init__(self):
        self.value = 0
        self.arduino = serial.Serial('/dev/ttyACM0', 9600)

    def getvalue(self, addr):
        if addr < 1 and addr > 3:
            return -1
        else:
            self.arduino.write("H".join(addr))
            s = self.arduino.readline()
            if s !="Recibido\n" :
                return -1
            else:
