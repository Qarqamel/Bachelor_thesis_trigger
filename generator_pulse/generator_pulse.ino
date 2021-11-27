//PROGRAMMABLE_PULSE_GENERATOR

#define PULSE_TIME_BASE_PIN 2
#define SIGNAL_PIN 5
#define FINISHED_PIN 6

#define PULSES_NR 10

struct Pulse{
  unsigned int start;
  unsigned int width;
};

struct Pulse sPulses[PULSES_NR] = {};
unsigned int Pulses[PULSES_NR*2];

void OnChange_PulseTimebase(){
  static unsigned int pulse_ctr = 0;
  static unsigned int tb_ctr = 0;
  tb_ctr++;
  if(tb_ctr >= Pulses[pulse_ctr]){
    tb_ctr = 0;
    pulse_ctr++;
    if(pulse_ctr == (PULSES_NR*2)){
      detachInterrupt(digitalPinToInterrupt(PULSE_TIME_BASE_PIN));
      digitalWrite(FINISHED_PIN, HIGH);
    }
    digitalWrite(SIGNAL_PIN, pulse_ctr%2);
  }  
}

void setup() {
  pinMode(SIGNAL_PIN, OUTPUT);
  pinMode(FINISHED_PIN, OUTPUT);
  pinMode(PULSE_TIME_BASE_PIN, INPUT_PULLUP);
  
  Serial.begin(115200);
  Serial.setTimeout(-1);
  Serial.println("COM opened;Waiting for pulses data");

  for(byte i = 0;i<PULSES_NR; i++){
    unsigned int pulse_start = Serial.readStringUntil('\n').toInt();
    unsigned int pulse_width = Serial.readStringUntil('\n').toInt();
    sPulses[i] = {pulse_start, pulse_width};
  }  
  Pulses[0] = sPulses[0].start;
  Pulses[1] = sPulses[0].width;
  for(unsigned int i = 1; i<PULSES_NR; i++){
    Pulses[2*i] = sPulses[i].start - (sPulses[i-1].start+sPulses[i-1].width);
    Pulses[(2*i)+1] = sPulses[i].width;
  }

  attachInterrupt(digitalPinToInterrupt(PULSE_TIME_BASE_PIN), OnChange_PulseTimebase, RISING);

  Serial.println("Started");
}

void loop() {
}
