int messwert=0;

void setup(){
  Serial.begin(9600);
}

void loop(){  
  messwert= analogRead(A0);
  Serial.print("Feuchtigkeits-Messwert:");
  Serial.println(messwert);
  delay(500);
} 
