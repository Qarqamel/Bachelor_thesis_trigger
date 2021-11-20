#define TIMEBASE_PIN 2
#define WAIT_TO_START_PIN 11
#define STARTED_PIN 13
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
  Serial1.print(sample_val);
  Sample_ctr++;
  if(sample_val == 1){
    sample_val = 0;
    Sample_ctr = 0;
  }    
}

void setup() {
  pinMode(TIMEBASE_PIN, INPUT_PULLUP);

  Serial1.begin(115200);
  Serial1.setTimeout(-1);
  Serial.begin(115200);
  Serial.setTimeout(-1);  

  Serial.println("Started");
  
  Serial.readStringUntil('\n');

  StartupSynchronization();
  attachInterrupt(digitalPinToInterrupt(TIMEBASE_PIN), OnChange_Timebase, RISING);
}

void loop() {
  Serial.readBytes(sample_val, 1);
  Serial1.readStringUntil('\n');
  Serial.println(Sample_ctr);
}
