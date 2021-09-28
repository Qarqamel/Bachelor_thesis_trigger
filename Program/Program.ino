#define SAMPLE_NR 400

#define ENABLE_INPUT_CAPTURE() (TIMSK1 |= (1<<ICIE1))
#define DISABLE_INPUT_CAPTURE() (TIMSK1 &= ~(1<<ICIE1))

unsigned int captured_times[SAMPLE_NR];
unsigned int sample_ctr = 0;
volatile bool acquisition_complete = false;

ISR(TIMER1_CAPT_vect){
  captured_times[sample_ctr++] = ICR1;
  if(sample_ctr == SAMPLE_NR){
    DISABLE_INPUT_CAPTURE();
    acquisition_complete = true;
  }
}

void setup() {

  pinMode(4, INPUT); //ICP1 pin - input capture pin. pin 4 - PD4 for Leonardo; pin 8 - PB0 for Uno
  TCCR1B = 0b01011010; //selecting edge for input capture, setting timer mode to CTC, and prescaler to 8
  
  Serial.begin(115200);
  Serial.setTimeout(-1);
}

void loop() {

  Serial.readStringUntil('\n');
  sample_ctr = 0;
  acquisition_complete = false;
  ENABLE_INPUT_CAPTURE();

  while(!acquisition_complete){}

  for(unsigned int i = 0; i < SAMPLE_NR; i++){
    Serial.println(captured_times[i]);
  }
}
