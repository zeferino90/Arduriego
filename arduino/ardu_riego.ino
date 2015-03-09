#include <TimerOne.h>

//Pin del sensor de temperatura
const int temp = A5;
//pins dels sensors de humitat
const int humitat1 = A4;
const int humitat2 = A3;
const int humitat3 = A3;
//pin del sensor nivell
const int nivell = A1;
//pins electrovalvulas
const int elect1 =;
const int elect2 =;
const int elect3 =;
const int elect4_5 =; //este controla las dos electrovalvulas de aguacorriente/deposito
boolean nivellPreparat = true;
const long tempsnopreparat = 300000000; //5 minuts que no es pot demanar
long tempsUs;

void setup(){
  Serial.begin(9600);
  pinMode(elect1, OUTPUT);
  pinMode(elect2, OUTPUT);
  pinMode(elect3, OUTPUT);
  pinMode(elect4_5, OUTPUT);
  Timer1.initialize(tempsnopreparat);//se supone 5 minutos
  Timer1.attachInterrupt(activarNivell);
}

void activarNivell(){
  nivellPreparat = true;
}

float temperatura(){
  int sensorVal = analogRead(temp);
  float voltatge = (sensorVal/1024.0) * 5.0;
  float temperatura = (voltatge - .5) * 100;
  return temperatura;
}

int sensorNivell(){
  return analogRead(nivell); 
}

int sensorHumitat(char h){
  if(h = '1') return analogRead(humitat1);
  else if(h = '2') return analogRead(humitat2);
  else if(h = '3') return analogRead(humitat3);
  return -1;
}

int obrirElectrovalvula(char e){
  if(e = '1') {
    digitalWrite(elect1, HIGH);
    return 0;
  }
  else if(e = '2'){
    digitalWrite(elect2, HIGH);
    return 0;
  }
  else if(e = '3'){
    digitalWrite(elect3, HIGH);
    return 0;
  }
  else if(e = '4'){
    digitalWrite(elect4_5, HIGH);
    return 0;
  }
  else return -1;
}

int tancarElectrovalvula(char e){
  if(e = '1') {
    digitalWrite(elect1, LOW);
    return 0;
  }
  else if(e = '2'){
    digitalWrite(elect2, LOW);
    return 0;
  }
  else if(e = '3'){
    digitalWrite(elect3, LOW);
    return 0;
  }
  else if(e = '4'){
    digitalWrite(elect4_5, LOW);
    return 0;
  }
  else return -1;
}

int consultarElectrovalvula(char e){
  if(e = '1') {
    return digitalRead(elect1);
  }
  else if(e = '2'){
    return digitalRead(elect2);
  }
  else if(e = '3'){
    return digitalRead(elect3);
  }
  else if(e = '4'){
    return digitalRead(elect4_5);
  }
  else return -1;
}

void loop(){
  if(nivellPreparat) noInterrupts(); 
  if (Serial.available()) { //Si está disponible
      String c = Serial.read(); //guardo la comanda
      if (c[0] == "T") { //Si es una 'T', enviar temperatura
        Serial.print("Recibido");
        Serial.print(temperatura());
      } else if (c[0] == "G") { //Si es una 'G', enviar dades gps
        Serial.print("Recibido");
        //falta gps
      }
      } else if (c[0] == "N") { //Si es una 'N', enviar dades sensor nivell
        Serial.print("Recibido");
        if(!nivellPreparat) Serial.println("No disponible");
        else{
          Serial.print(sensorNivell());
          nivellPreparat = false;
          interrupts();
        }
      }
      } else if (c[0] == "H") { //Si es una 'H', enviar dades sensor humitat
        Serial.print("Recibido");
        Serial.print(sensorHumitat(c[1]));
      }
      } else if (c[0] == "E") { //Si es una 'E', obrir o tancar una electrovalvula
        Serial.print("Recibido");
        if (c[1] = 'O') Serial.print(obrirElectrovalvula(c[2]));
        else if(c[1] = 'T') Serial.print(tancarElectrovalvula(c[2]));
        else if(c[1] = 'C') Serial.print(consultarElectrovalvula(c[2]));
      }
   }
}
