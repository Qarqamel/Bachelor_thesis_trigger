#define SAMPLE_NR 470

unsigned int captured_times[SAMPLE_NR];
unsigned int captured_time_prev;
unsigned int tbl_iter = 0;

ISR(TIMER1_CAPT_vect){
  //TCNT1 = 0;
  captured_times[tbl_iter++] = ICR1 - captured_time_prev;
  captured_time_prev = ICR1;
  if(tbl_iter == SAMPLE_NR)
    tbl_iter = 0;
}

void setup() {
  // put your setup code here, to run once:
  pinMode(4, INPUT); //ICP1 pin - input capture pin. pin 4 - PD4 for Leonardo; pin 8 - PB0 for Uno
  TCCR1B = 0b01011010;
  TIMSK1 |= 0b00100000;
  SREG |= 0b10000000;
  
  Serial.begin(115200);
  Serial.setTimeout(-1);
}

void loop() {

  Serial.readStringUntil('\n');
  TIMSK1 &= 0b11011111;
  for(unsigned int i = 0; i < SAMPLE_NR; i++){
    Serial.println(captured_times[i]);
  }
  TIMSK1 |= 0b00100000;
}
