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
const int valv1 =2;
const int valv2 =3;
const int valv3 =4;
const int valv4_5 =5; //este controla las dos electrovalvulas de aguacorriente/deposito
boolean levelReady = true;
const long tempsnopreparat = 300000000; //5 minuts que no es pot demanar
long tempsUs;
char* c;

void setup(){
  Serial.begin(9600);
  Serial.setTimeout(1000);//Timeout esperando en lecturas 1000 milis
  pinMode(valv1, OUTPUT);
  pinMode(valv2, OUTPUT);
  pinMode(valv3, OUTPUT);
  pinMode(valv4_5, OUTPUT);
  Timer1.initialize(tempsnopreparat);//se supone 5 minutos
  Timer1.attachInterrupt(activarNivell);
}

void activarNivell(){
  levelReady = true;
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
    digitalWrite(valv1, HIGH);
    return 0;
  }
  else if(e = '2'){
    digitalWrite(valv2, HIGH);
    return 0;
  }
  else if(e = '3'){
    digitalWrite(valv3, HIGH);
    return 0;
  }
  else if(e = '4'){
    digitalWrite(valv4_5, HIGH);
    return 0;
  }
  else return -1;
}

int tancarElectrovalvula(char e){
  if(e = '1') {
    digitalWrite(valv1, LOW);
    return 0;
  }
  else if(e = '2'){
    digitalWrite(valv2, LOW);
    return 0;
  }
  else if(e = '3'){
    digitalWrite(valv3, LOW);
    return 0;
  }
  else if(e = '4'){
    digitalWrite(valv4_5, LOW);
    return 0;
  }
  else return -1;
}

int consultarElectrovalvula(char e){
  if(e = '1') {
    return digitalRead(valv1);
  }
  else if(e = '2'){
    return digitalRead(valv2);
  }
  else if(e = '3'){
    return digitalRead(valv3);
  }
  else if(e = '4'){
    return digitalRead(valv4_5);
  }
  else return -1;
}

void loop(){
  if(levelReady) noInterrupts(); 
  if (Serial.available()) { //Si está disponible
      Serial.readBytes(c, 2); //guardo la comanda, en general son 2 caracters per aixo llegeixo dos, si es una comanda d'un sol caracter saltara el timeout i nomes llegira un
      if (*c == 'T') { //Si es una 'T', enviar temperatura
        Serial.print("Recibido\n");
        Serial.print(temperatura());
      } else if (*c == 'G') { //Si es una 'G', enviar dades gps
        Serial.print("Recibido\n");
        //falta gps
      }
    
     else if (*c == 'N') { //Si es una 'N', enviar dades sensor nivell
       Serial.print("Recibido\n");
       if(!levelReady) Serial.println("No disponible\n");
       else{
         Serial.print(sensorNivell());
         levelReady = false;
         interrupts();
       }
     }
     else if (*c == 'H') { //Si es una 'H', enviar dades sensor humitat
       Serial.print("Recibido\n");
       c++;
       Serial.print(sensorHumitat(*c));
     }
     else if (*c == 'E') { //Si es una 'E', obrir o tancar una electrovalvula
       Serial.print("Recibido\n");
       c++;
       if (*c = 'O') Serial.print(obrirElectrovalvula(c[2]));
       else if(*c = 'C') Serial.print(tancarElectrovalvula(c[2]));
       else if(*c = 'G') Serial.print(consultarElectrovalvula(c[2]));
     }
  }
}
