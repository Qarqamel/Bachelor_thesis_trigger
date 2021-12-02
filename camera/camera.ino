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

#define SIGNAL_CH1_PIN 4
#define SIGNAL_CH0_PIN 3
#define SAMPLE_PIN 2

void OnChange_Sample(){
  byte read_bit_ch1 = digitalRead(SIGNAL_CH0_PIN);
  byte read_bit_ch2 = digitalRead(SIGNAL_CH1_PIN);
  Serial.print((read_bit_ch2<<1)|read_bit_ch1);
}

void setup() {
  pinMode(SIGNAL_CH0_PIN, INPUT_PULLUP);
  pinMode(SIGNAL_CH1_PIN, INPUT_PULLUP);
  pinMode(SAMPLE_PIN, INPUT_PULLUP);
    
  Serial.begin(115200);
  Serial.setTimeout(-1);

  attachInterrupt(digitalPinToInterrupt(SAMPLE_PIN), OnChange_Sample, RISING);
  
  Serial.println("Started");
}

void loop() {
}
