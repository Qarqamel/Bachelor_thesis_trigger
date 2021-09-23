#define SAMPLE_NR 400

unsigned long times[SAMPLE_NR]; //= {0,11,22,33,44,55,66, 77, 88, 99};
unsigned int times_iter = 0;

void Interrupt_routine(){
  times[times_iter++] = micros();
  if(times_iter == SAMPLE_NR){
    detachInterrupt(digitalPinToInterrupt(2));
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.setTimeout(-1);

  pinMode(2, INPUT);
  attachInterrupt(digitalPinToInterrupt(2), Interrupt_routine, RISING);
  }

void loop() {
  Serial.readStringUntil('\n');

  detachInterrupt(digitalPinToInterrupt(2));
  
  for(unsigned int i = 0; i < SAMPLE_NR; i++){
    Serial.println(times[i]);
  }
  times_iter = 0;
  attachInterrupt(digitalPinToInterrupt(2), Interrupt_routine, RISING);
}
