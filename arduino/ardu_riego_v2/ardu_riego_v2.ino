char c[50];
int i = 0;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1000);
}

void loop(){
  int bytes=Serial.available();
  for(int i=0; i<bytes; i++){
    c[i]=Serial.read();
  }
  Serial.print(c);
}
