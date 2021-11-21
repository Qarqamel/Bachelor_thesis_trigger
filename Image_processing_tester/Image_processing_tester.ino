#define TIMEBASE_PIN 2
#define WAIT_TO_START_PIN 11
#define STARTED_PIN 13

#define SAMPLE_CH_bm 0
#define STOP_CH_bm 1

#define TB_sr Serial
#define Sig_proc_sr Serial1

#define PULSES_NR_PER_ACQ 100

void StartupSynchronization(){
  pinMode(WAIT_TO_START_PIN, INPUT_PULLUP);
  pinMode(STARTED_PIN, INPUT_PULLUP);
  while(digitalRead(WAIT_TO_START_PIN)){}
  pinMode(STARTED_PIN, OUTPUT);
  digitalWrite(STARTED_PIN, 0);
}

volatile unsigned long Sample_ctr = 0;
volatile byte sample_val = 0;

void OnChange_Timebase(){
  Sig_proc_sr.print(sample_val);
  Sample_ctr++;
  if(sample_val>0){
    sample_val = 0;
    Sample_ctr = 0;
  }    
}

void setup() {
  pinMode(TIMEBASE_PIN, INPUT_PULLUP);

  Sig_proc_sr.begin(115200);
  Sig_proc_sr.setTimeout(-1);
  TB_sr.begin(115200);
  TB_sr.setTimeout(-1);
  
  TB_sr.println("Started");
  TB_sr.readStringUntil('\n');

  StartupSynchronization();
  attachInterrupt(digitalPinToInterrupt(TIMEBASE_PIN), OnChange_Timebase, RISING);
}

void loop() {
  sample_val = TB_sr.readStringUntil('\n').toInt();
  TB_sr.println(Sig_proc_sr.readStringUntil('\n'));
  TB_sr.println(Sample_ctr);
}
