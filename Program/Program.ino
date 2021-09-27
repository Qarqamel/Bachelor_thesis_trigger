#define SAMPLE_NR 400

unsigned long times[SAMPLE_NR];
unsigned int times_iter = 0;
volatile bool acquisition_complete = false;

void Interrupt_routine(){
  times[times_iter++] = micros();
  if(times_iter == SAMPLE_NR){
    detachInterrupt(digitalPinToInterrupt(2));
    acquisition_complete = true;
  }
}

void setup() {

  Serial.begin(115200);
  Serial.setTimeout(-1);

  pinMode(2, INPUT);
  }

void loop() {
  Serial.readStringUntil('\n');
  times_iter = 0;
  acquisition_complete = false;  
  attachInterrupt(digitalPinToInterrupt(2), Interrupt_routine, RISING);

  while(!acquisition_complete){}
  
  for(unsigned int i = 0; i < SAMPLE_NR; i++){
    Serial.println(times[i]);
  }
}
