//#include <TimerOne.h>
#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>

SoftwareSerial mySerial(3, 2);

//Pin del sensor de temperatura
const int temp = A5;
//pins dels sensors de humitat
const int humitat1 = A2;
const int humitat2 = A3;
const int humitat3 = A4;
//pin del sensor nivell
const int nivell = A1;
//pins electrovalvulas
const int valv1 =4;
const int valv2 =5;
const int valv3 =6;
const int valv4_5 =7; //este controla las dos electrovalvulas de aguacorriente/deposito
boolean levelReady = true;
const long tempsnopreparat = 60000; //1 minuts que no es pot demanar
unsigned long t;
long tempsUs;
char c[5];
int ic;
int i;
bool stringComplete;
boolean usingInterrupt = false;
Adafruit_GPS GPS(&mySerial);

void setup(){
  Serial.begin(115200);
  //Serial.setTimeout(1000);//Timeout esperando en lecturas 1000 milis
  pinMode(valv1, OUTPUT);
  pinMode(valv2, OUTPUT);
  pinMode(valv3, OUTPUT);
  pinMode(valv4_5, OUTPUT);
  GPS.begin(9600);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA); //turn on RMC (recommended minimum) and GGA (fix data) including altitude
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate
  GPS.sendCommand(PGCMD_ANTENNA);
  useInterrupt(true);
}

SIGNAL(TIMER0_COMPA_vect) {
  char c = GPS.read();
  // if you want to debug, this is a good time to do it!
/*#ifdef UDR0
  if (GPSECHO)
    if (c) UDR0 = c;  
    // writing direct to UDR0 is much much faster than Serial.print 
    // but only one character can be written at a time. 
#endif*/
}

void useInterrupt(boolean v) {
  if (v) {
    // Timer0 is already used for millis() - we'll just interrupt somewhere
    // in the middle and call the "Compare A" function above
    OCR0A = 0xAF;
    TIMSK0 |= _BV(OCIE0A);
    usingInterrupt = true;
  } else {
    // do not call the interrupt function COMPA anymore
    TIMSK0 &= ~_BV(OCIE0A);
    usingInterrupt = false;
  }
}

void stateGPS(){
  Serial.print("\nTime: ");
  Serial.print(GPS.hour, DEC); Serial.print(':');
  Serial.print(GPS.minute, DEC); Serial.print(':');
  Serial.print(GPS.seconds, DEC); Serial.print('.');
  Serial.println(GPS.milliseconds);
  Serial.print("Date: ");
  Serial.print(GPS.day, DEC); Serial.print('/');
  Serial.print(GPS.month, DEC); Serial.print("/20");
  Serial.println(GPS.year, DEC);
  Serial.print("Fix: "); Serial.print((int)GPS.fix);
  Serial.print(" quality: "); Serial.println((int)GPS.fixquality); 
  if (GPS.fix) {
    Serial.print("Location: ");
    Serial.print(GPS.latitude, 4); Serial.print(GPS.lat);
    Serial.print(", "); 
    Serial.print(GPS.longitude, 4); Serial.println(GPS.lon);
    Serial.print("Location (in degrees, works with Google Maps): ");
    Serial.print(GPS.latitudeDegrees, 4);
    Serial.print(", "); 
    Serial.println(GPS.longitudeDegrees, 4);
      
    Serial.print("Speed (knots): "); Serial.println(GPS.speed);
    Serial.print("Angle: "); Serial.println(GPS.angle);
    Serial.print("Altitude: "); Serial.println(GPS.altitude);
    Serial.print("Satellites: "); Serial.println((int)GPS.satellites);
  }
}

float temperatura(){
  int sensorVal = analogRead(temp);
//  Serial.print("SensorVal: ");
//  Serial.print(sensorVal);
//  Serial.print("\n");
  float voltatge = (sensorVal/1024.0) * 4.3; //el voltatge rel es 4.3V
//  Serial.print("Vol: ");
//  Serial.print(voltatge);
//  Serial.print("\n");
  float temperatura = (voltatge - .5) * 100;
  return temperatura;
}

int sensorNivell(){
  //VALOR > 500 totalmente sumergido, si no vacio
  levelReady = false;
  t = millis();
  return analogRead(nivell); 
}

int sensorHumitat(char h){
  if(h == '1') return analogRead(humitat1);
  else if(h == '2') return analogRead(humitat2);
  else if(h == '3') return analogRead(humitat3);
  return -1;
}

int obrirElectrovalvula(char e){
  if(e == '1') {
    digitalWrite(valv1, HIGH);
    return 0;
  }
  else if(e == '2'){
    digitalWrite(valv2, HIGH);
    return 0;
  }
  else if(e == '3'){
    digitalWrite(valv3, HIGH);
    return 0;
  }
  else if(e == '4'){
    digitalWrite(valv4_5, HIGH);
    return 0;
  }
  else return -1;
}

int tancarElectrovalvula(char e){
  if(e == '1') {
    digitalWrite(valv1, LOW);
    return 0;
  }
  else if(e == '2'){
    digitalWrite(valv2, LOW);
    return 0;
  }
  else if(e == '3'){
    digitalWrite(valv3, LOW);
    return 0;
  }
  else if(e == '4'){
    digitalWrite(valv4_5, LOW);
    return 0;
  }
  else return -1;
}

int consultarElectrovalvula(char e){
  if(e == '1') {
    return digitalRead(valv1);
  }
  else if(e == '2'){
    return digitalRead(valv2);
  }
  else if(e == '3'){
    return digitalRead(valv3);
  }
  else if(e == '4'){
    return digitalRead(valv4_5);
  }
  else return -1;
}

void serialEvent(){
  while (Serial.available()) {
    //Serial.print("añadido nuevo caracter: ");
    char inChar = Serial.read(); 
//    Serial.print(inChar);
//    Serial.print(" ");
//    Serial.print(ic);
//    Serial.print("\n");
    c[ic] = inChar;
    ic++;
    if (inChar == '\n') {
      stringComplete = true;
//      Serial.print("Terminado de leer\n");
      ic = 0;
    } 
  }
}

void loop(){
  GPS.parse(GPS.lastNMEA());
  if(!levelReady) {
    if(millis() - t > tempsnopreparat) levelReady = true;
  }
  
   //Si está disponible
   
//      if(stringComplete){
//        Serial.print(c);
//        stringComplete = false;
//        ic = 0;
//      }

      if (c[0] == 'T' and stringComplete) { //Si es una 'T', enviar temperatura
        c[0] = '0';
        Serial.print("Recibido\n");
        Serial.print(temperatura());
        Serial.print("\n");
        stringComplete = false;
        ic = 0;
      } 
      else if (c[0] == 'G' and stringComplete) { //Si es una 'G', enviar dades gps
        c[0] = '0';
        Serial.print("Recibido\n");
        if(c[1] == 'F'){
          if(GPS.fix) {
            Serial.print("True");
            Serial.print("\n");
          }
          else {
            Serial.print("False");
            Serial.print("\n");
          }
        }
        else if(c[1] == 'C'){  
          if(GPS.fix){
            Serial.print(GPS.latitudeDegrees, 4);
            Serial.print(" ");
            Serial.print(GPS.longitudeDegrees, 4);
            Serial.print("\n");
          }
          else{
            Serial.print("No fix\n");
          }
        }
        else if(c[1] == 'S'){
          stateGPS();
        }
        stringComplete = false;
        ic = 0;
      }
    
     else if (c[0] == 'N' and stringComplete) { //Si es una 'N', enviar dades sensor nivell
       c[0] = '0';
       Serial.print("Recibido\n");
       if(!levelReady) Serial.println("-1\n");
       else{
         Serial.print(sensorNivell());
         Serial.print("\n");
       }
       stringComplete = false;
        ic = 0;
     }
     else if (c[0] == 'H' and stringComplete) { //Si es una 'H', enviar dades sensor humitat
       c[0] = '0';
       Serial.print("Recibido\n");
       Serial.print(sensorHumitat(c[1]));
       Serial.print("\n");
       stringComplete = false;
        ic = 0;
     }
     else if (c[0] == 'E' and stringComplete) { //Si es una 'E', obrir o tancar una electrovalvula
       c[0] = '0';
       Serial.print("Recibido\n");
       if (c[1] == 'O') {
         Serial.print(obrirElectrovalvula(c[2]));
         Serial.print("\n");
       }
       else if(c[1] == 'C') {
         Serial.print(tancarElectrovalvula(c[2]));
         Serial.print("\n");
       }
       else if(c[1] == 'G') {
         Serial.print(consultarElectrovalvula(c[2]));
         Serial.print("\n");
       }
       stringComplete = false;
       ic = 0;
     }
}
