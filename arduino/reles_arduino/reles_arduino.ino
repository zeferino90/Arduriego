int Relay1= 2;
int Relay2= 3;
int Relay3= 4;
int Relay4= 5;

void setup(){
  pinMode(Relay1, OUTPUT);
  pinMode(Relay2, OUTPUT);
  pinMode(Relay3, OUTPUT);
  pinMode(Relay4, OUTPUT);
}

void loop(){
  delay(3000);
    digitalWrite(Relay1, LOW);
    digitalWrite(Relay2, LOW);
    digitalWrite(Relay3, LOW);
    digitalWrite(Relay4, LOW);
  delay(2000);
    digitalWrite(Relay1, HIGH);
    digitalWrite(Relay2, LOW);
    digitalWrite(Relay3, LOW);
    digitalWrite(Relay4, LOW);
  delay(2000);
    digitalWrite(Relay1, LOW);
    digitalWrite(Relay2, HIGH);
    digitalWrite(Relay3, LOW);
    digitalWrite(Relay4, LOW);
  delay(2000);
    digitalWrite(Relay1, LOW);
    digitalWrite(Relay2, LOW);
    digitalWrite(Relay3, HIGH);
    digitalWrite(Relay4, LOW);
  delay(2000);
    digitalWrite(Relay1, LOW);
    digitalWrite(Relay2, LOW);
    digitalWrite(Relay3, LOW);
    digitalWrite(Relay4, HIGH);
  }

