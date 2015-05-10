import serial
 
arduino = serial.Serial('/dev/ttyACM0', 115200)
 
print("Starting!")
 
while True:
      comando = raw_input('Introduce un comando: ') #Input
      arduino.write(comando) #Mandar un comando hacia Arduino
      s = arduino.readline()
      print s
      print("\n")
      s = arduino.readline()
      print s
      print("\n")
      #if comando == 'H':
      #      print('LED ENCENDIDO')
      #elif comando == 'L':
      #      print('LED APAGADO')
 
arduino.close() #Finalizamos la comunicacion