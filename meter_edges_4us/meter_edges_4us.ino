//METER
//
//Mierzy czas(us)od resetu na zboczach PWM-a wejściowego.
//Okres wejściowy: 0-4294967295us
//
//INPUT: 2-PD2(Uno), 2-PD1(Leonardo)
//OUTPUT: -
//
//Na rosnących zboczach wejściowego PWM-a, mierzy czas(us) od resetu, a następnie wysyła pomiar przez UART.

//przetestowane dla 5ms

#define TSTAMP_NR           10

#define TIMEBASE_PIN        2
#define EDGE_PIN            3

volatile unsigned long time_base_ctr = 0;
volatile unsigned long Pulses_times[TSTAMP_NR];
volatile byte pulse_ctr = 0;
volatile bool acquisition_complete = false;

void OnChange_Timebase(){
  time_base_ctr++;
}

void OnChange_Edge(){
  Pulses_times[pulse_ctr++] = time_base_ctr;
  if(pulse_ctr == TSTAMP_NR)
    acquisition_complete = true;
}

void setup(){
  pinMode(TIMEBASE_PIN, INPUT_PULLUP);
  pinMode(EDGE_PIN, INPUT_PULLUP);

  Serial.begin(115200);
  Serial.setTimeout(-1);
  Serial.println("COM opened");

  attachInterrupt(digitalPinToInterrupt(TIMEBASE_PIN), OnChange_Timebase, RISING);
  attachInterrupt(digitalPinToInterrupt(EDGE_PIN), OnChange_Edge, RISING);

  Serial.println("Started");
  
  while(!acquisition_complete){}
  for(byte i = 0; i<TSTAMP_NR; i++){
    Serial.println(Pulses_times[i]);
  }
}

void loop(){
}
