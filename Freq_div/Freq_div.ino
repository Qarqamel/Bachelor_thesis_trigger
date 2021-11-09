#define SIGNEL_PIN 2
#define OUTPUT_PIN 5

volatile unsigned int ctr=0;
unsigned int max_ctr_val=100;

void OnSignalChange(){
  ctr++;
  if(ctr>=max_ctr_val){
    ctr=0;
    digitalWrite(OUTPUT_PIN, !digitalRead(OUTPUT_PIN));
  }
}

void setup() {
  // put your setup code here, to run once:
  pinMode(2, INPUT);
  pinMode(5, OUTPUT);
  
  attachInterrupt(digitalPinToInterrupt(2), OnSignalChange, RISING);

  Serial.begin(115200);
  Serial.setTimeout(-1);
}

void loop() {
  // put your main code here, to run repeatedly:
  max_ctr_val = Serial.readStringUntil('\n').toInt();
}
