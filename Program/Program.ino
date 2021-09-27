#define SAMPLE_NR 400
#define ICIE1_bm (1<<ICIE1)

unsigned int captured_times[SAMPLE_NR];
unsigned int captured_time_prev;
unsigned int tbl_iter = 0;
volatile bool acquisition_complete = false;

ISR(TIMER1_CAPT_vect){
  captured_times[tbl_iter++] = ICR1 - captured_time_prev;
  captured_time_prev = ICR1;
  if(tbl_iter == SAMPLE_NR){
    TIMSK1 &= ~ICIE1_bm; //disable timer input capture interrupts
    acquisition_complete = true;
  }
}

void setup() {

  pinMode(4, INPUT); //ICP1 pin - input capture pin. pin 4 - PD4 for Leonardo; pin 8 - PB0 for Uno
  TCCR1B = 0b01011010; //enable timer input capture interrupts
  
  Serial.begin(115200);
  Serial.setTimeout(-1);
}

void loop() {

  Serial.readStringUntil('\n');
  tbl_iter = 0;
  acquisition_complete = false;
  TIMSK1 |= ICIE1_bm;

  while(!acquisition_complete){}
  
  while(TIMSK1&ICIE1_bm == ICIE1_bm){}

  for(unsigned int i = 0; i < SAMPLE_NR; i++){
    Serial.println(captured_times[i]);
  }
}
