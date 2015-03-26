import serial

__author__ = 'zeferino'
class humidity_sensor:
    def __init__(self):
        self.value = 0
        self.arduino = serial.Serial('/dev/ttyACM0', 115200, timeout= 1.0)

    def getvalue(self, addr):
        result = 0
        if addr < 1 and addr > 3:
            result = -1
        else:
            self.arduino.write("H".join(addr))
            s = self.arduino.readline()
            if s !="Recibido\n":
                result = -1
            else:
                s = self.arduino.readline()
                sresult=s[0: s.len - 2]
                result=int(sresult)
        return result
    '''falta saber si la conversion de sresult es correcta, falta descubrir que devuelve el sensor i que ranog de valores devuelve'''