#define WAIT_TO_START_PIN 11
#define STARTED_PIN 13
#define PULSE_OUT_PIN 4
#define PULSE_IN_PIN 3


void StartupSynchronization(){
  pinMode(WAIT_TO_START_PIN, INPUT_PULLUP);
  pinMode(STARTED_PIN, INPUT_PULLUP);
  while(digitalRead(WAIT_TO_START_PIN)){}
  pinMode(STARTED_PIN, OUTPUT);
  digitalWrite(STARTED_PIN, 0);
}

void setup() {
  pinMode(PULSE_IN_PIN, INPUT_PULLUP);
  pinMode(PULSE_OUT_PIN, OUTPUT);
  
  Serial.begin(115200);
  Serial.setTimeout(-1);
  Serial.println("Started");

  StartupSynchronization();
}

void loop() {
  Serial.readStringUntil('\n');
  unsigned long Time_of_pulse = micros();
  digitalWrite(PULSE_OUT_PIN, HIGH);
  while(!PULSE_IN_PIN){}
  unsigned long Delay = micros() - Time_of_pulse;
  digitalWrite(PULSE_OUT_PIN, LOW);
  Serial.println(Delay);
}
