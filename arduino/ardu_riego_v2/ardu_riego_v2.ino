char c[5];
int i = 0;
int primercop = 0;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1000);
}

void loop(){
  int bytes=Serial.available();
  for(int i=0; i<bytes; i++){
    c[i]=Serial.read();
    primercop = 1;
  }
  if(primercop == 1){
    primercop = 0;
    Serial.print(c);
  }
  
}
