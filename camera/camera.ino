//CAMERA
//
//Zwraca stan na pinie 3 na każym rosnący zboczu przebiegu na pinie 2.
//
//INPUT: INPUT: 2-PD2(Uno), 2-PD1(Leonardo), 3-PD3(Uno), 3-PD0(Leonardo)
//OUTPUT: -
//
//Zbocza rosnące przebiegu podanego na pin 2 uruchamiją przerwanie, w którym stan pinu 3 jest odczytywany oraz wysyłany przez UART.
//
//Testy dzialaja tylko na Uno, bo resetuje sie przy otwieraniu portu

#define SR_SYNC 1

#define WAIT_TO_START_PIN 11
#define STARTED_PIN 13
#define SIGNAL_CH2_PIN 4
#define SIGNAL_CH1_PIN 3
#define SAMPLE_PIN 2

void StartupSynchronization(){
  pinMode(WAIT_TO_START_PIN, INPUT_PULLUP);
  pinMode(STARTED_PIN, INPUT_PULLUP);
  while(digitalRead(WAIT_TO_START_PIN)){}
  pinMode(STARTED_PIN, OUTPUT);
  digitalWrite(STARTED_PIN, 0);
}

void OnChange_Sample(){
  byte read_bit_ch1 = digitalRead(SIGNAL_CH1_PIN);
  byte read_bit_ch2 = digitalRead(SIGNAL_CH2_PIN);
  Serial.print((read_bit_ch2<<1)|read_bit_ch1);
}

void setup() {
  pinMode(SIGNAL_CH1_PIN, INPUT_PULLUP);
  pinMode(SIGNAL_CH2_PIN, INPUT_PULLUP);
  pinMode(SAMPLE_PIN, INPUT_PULLUP);
    
  Serial.begin(115200);
  Serial.setTimeout(-1);
  Serial.println("Init");
  if(!SR_SYNC){
    Serial.readStringUntil('\n');
    StartupSynchronization();
  }
  attachInterrupt(digitalPinToInterrupt(SAMPLE_PIN), OnChange_Sample, RISING);
  if (SR_SYNC){
    Serial.println("Started");
  }
}

void loop() {
}
