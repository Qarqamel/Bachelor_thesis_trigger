#define SAMPLE_NR 400

unsigned int captured_times[SAMPLE_NR];
unsigned int captured_time_prev;
unsigned int tbl_iter = 0;
//bool meter_active_flag = false;

ISR(TIMER1_CAPT_vect){
  captured_times[tbl_iter++] = ICR1 - captured_time_prev;
  captured_time_prev = ICR1;
  if(tbl_iter == SAMPLE_NR)
    TIMSK1 &= 0b11011111;
    //meter_active_flag = false;
}

void setup() {
  // put your setup code here, to run once:
  pinMode(4, INPUT); //ICP1 pin - input capture pin. pin 4 - PD4 for Leonardo; pin 8 - PB0 for Uno
  TCCR1B = 0b01011010;
  
  Serial.begin(9600);
  Serial.setTimeout(-1);
}

void loop() {

  Serial.readStringUntil('\n');
  //meter_active_flag = true;
  tbl_iter = 0;
  TIMSK1 |= 0b00100000;

  //while(meter_active_flag){}
  while(TIMSK1&0b00100000 == 0b00100000){}

  for(unsigned int i = 0; i < SAMPLE_NR; i++){
    Serial.println(captured_times[i]);
  }
}
