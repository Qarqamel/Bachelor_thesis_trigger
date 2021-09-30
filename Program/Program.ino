#define SAMPLE_NR 2900

#define ENABLE_INPUT_CAPTURE() (TIMSK4 |= (1<<ICIE4))
#define DISABLE_INPUT_CAPTURE() (TIMSK4 &= ~(1<<ICIE4))

volatile unsigned int Periods[SAMPLE_NR];
volatile unsigned int Period_prev;
volatile unsigned int edge_ctr = 0;
volatile bool acquisition_complete = false;
volatile bool first_acq = false;

ISR(TIMER4_CAPT_vect){
  Periods[edge_ctr++] = ICR4 - Period_prev;
  Period_prev = ICR4;
  if(first_acq){
    edge_ctr--;
    first_acq = false;
  }
  if(edge_ctr == SAMPLE_NR){
    DISABLE_INPUT_CAPTURE();
    acquisition_complete = true;
  }
}

void setup() {

  pinMode(8, INPUT); //ICP1 pin - input capture pin. pin 4 - PD4 for Leonardo; pin 8 - PB0 for Uno;ICP4 pin 49 - PL1 for Mega
  
  //ICES - input capture edge select to rising, CS - setting prescaler to 8
  //WGM - setting waveform generation mode to 0
  TCCR4B |= (1<<ICES4)|(1<<CS41);
  TCCR4B &= ~((1<<ICNC4)|(1<<WGM43)|(1<<WGM42)|(1<<CS42)|(1<<CS40));
  TCCR4A &= ~((1<<COM4A1)|(1<<COM4A0)|(1<<COM4B1)|(1<<COM4B0)|(1<<COM4C1)|(1<<COM4C0)|(1<<WGM41)|(1<<WGM40));
  
  
  Serial.begin(115200);
  Serial.setTimeout(-1);

  Serial.println("ready");
}

void loop() {

  Serial.readStringUntil('\n');
  edge_ctr=0;
  acquisition_complete=false;
  first_acq = true;
  ENABLE_INPUT_CAPTURE();

  while(!acquisition_complete){}

  for(unsigned int i=0; i<SAMPLE_NR; i++){
    Serial.println(Periods[i]);
  }
}
