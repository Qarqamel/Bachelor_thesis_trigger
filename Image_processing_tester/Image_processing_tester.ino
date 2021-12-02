#define TIMEBASE_PIN 2
#define WAIT_FOR_PULSE_PIN 3

#define SAMPLE_CH_bm 0
#define STOP_CH_bm 1

#define Img_proc_sr Serial
#define TB_sr Serial1

#define PULSES_NR_PER_ACQ 100

volatile unsigned long Sample_ctr = 0;
volatile unsigned long Sample_ctr_buff = 0;
volatile byte sample_val = 0;
volatile bool waiting_for_pulse = true;

void OnChange_WaitForPulse(){
  Sample_ctr_buff = Sample_ctr;
  waiting_for_pulse = false;
}

void OnChange_Timebase(){
  Img_proc_sr.print(sample_val);
  Sample_ctr++;
  if(sample_val>0){
    sample_val = 0;
    Sample_ctr = 0;
  }
}

void setup() {
  pinMode(TIMEBASE_PIN, INPUT_PULLUP);
  pinMode(WAIT_FOR_PULSE_PIN, INPUT_PULLUP);

  TB_sr.begin(115200);
  TB_sr.setTimeout(-1);
  Img_proc_sr.begin(115200);
  Img_proc_sr.setTimeout(-1);
  
  attachInterrupt(digitalPinToInterrupt(TIMEBASE_PIN), OnChange_Timebase, RISING);
  attachInterrupt(digitalPinToInterrupt(WAIT_FOR_PULSE_PIN), OnChange_WaitForPulse, RISING);
  Img_proc_sr.println("Started");
}

void loop() {
  sample_val = TB_sr.readStringUntil('\n').toInt();
  while(waiting_for_pulse){}
  waiting_for_pulse = true;
  TB_sr.println(Sample_ctr_buff);
}
