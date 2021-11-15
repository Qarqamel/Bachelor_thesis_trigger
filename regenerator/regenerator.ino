//TRIGGER
//
//Generuje PWM o okresie proporcjonalnym do okresu PWM-a na wejściu. Pozwala na dostosowanie współczynnika proporcjonalności.
//Okres: 0-4095us
//Współczynnik proporcjonalności (T_in/T_out) jest ustawiany poprzez wysłanie uartem okresu jaki układ powinien generować dla aktulanego T_in.
//
//INPUT: 2-PD2(Uno), 2-PD1(Leonardo)
//OUTPUT: 10-PB2(Uno), 10-PB6(Leonardo)
//
//Mierzy okres PWM-a na wejściu przy użyciu przerwań oraz funkcji micros().
//Przy użyciu 16-bitowego timera (timer1) pracującego w trybie non inverting fast PWM z prescalerem 1, 
//generuje przebieg prostokątny o okresie proporcjonalnym do okresu PWM-a wejściowego.
//Na UART-cie odbiera okres(us), który ma zostać wygenerowany na wyjściu - co prowadzi do dostosowania współczynnika proporcjonalności,
//względem aktualnego okresu wejściowego.

#define TIMEBASE_PIN 2
#define WAIT_TO_START_1_PIN 11
#define WAIT_TO_START_2_PIN 12
#define STARTED_PIN 13

void StartupSynchronization(){
  pinMode(WAIT_TO_START_1_PIN, INPUT_PULLUP);
  pinMode(WAIT_TO_START_2_PIN, INPUT_PULLUP);
  pinMode(STARTED_PIN, INPUT_PULLUP);
  while(digitalRead(WAIT_TO_START_1_PIN)||digitalRead(WAIT_TO_START_2_PIN)){}
  pinMode(STARTED_PIN, OUTPUT);
  digitalWrite(STARTED_PIN, 0);
}

void TimerConfig(){
  DDRB |= (1<<PB2); //alternatively pinMode(10, OUT);(PB2 - Uno, PB6 Leonardo) - setting pin connected to sqr_wave_gen direction to output
  TCCR1A |= (1<<WGM11)|(1<<WGM10); //COM1A0|WGM11|WGM10 - non inverting, fast PWM mode, TOP in OCR1A
  TCCR1A &= ~((1<<COM1A1)|(1<<COM1A0)|(1<<COM1B0)|(1<<COM1B1));
  TCCR1B |= (1<<WGM13)|(1<<WGM12); //further setting timer mode and setting prescaler to 0(clock disabled)
  TCCR1B &= ~((1<<ICNC1)|(1<<ICES1)|(1<<CS12)|(1<<CS11)|(1<<CS10));
}

void TimerStart(){
  TCCR1A |= (1<<COM1B1);
}

volatile unsigned int T_out;
unsigned long T_in;
float Coeficient = 100; // T_in/T_out
byte irq_ctr = 0;
volatile bool callib = false;

void OnChange_Timebase(){
  static unsigned long micro_sec_curr, micro_sec_prev;
  
  micro_sec_curr = micros();
  T_in = micro_sec_curr - micro_sec_prev;
  micro_sec_prev = micro_sec_curr;
  if (callib){
  Coeficient = T_in/T_out;
  }
  OCR1A = (T_in*16)/Coeficient;  
  OCR1B = OCR1A/2;
  
  irq_ctr++;
  if(irq_ctr==2){
    TCCR1B |= (1<<CS10); //aktywacja timera - prescaler ustawiony na 1
  }
}

void setup() {
  pinMode(TIMEBASE_PIN, INPUT_PULLUP);
  
  Serial.begin(115200);
  Serial.setTimeout(-1);
  Serial.println("Started");
    
  TimerConfig();
  StartupSynchronization();
  attachInterrupt(digitalPinToInterrupt(TIMEBASE_PIN), OnChange_Timebase, RISING);
  TimerStart();
}

void loop() {  
  T_out = Serial.readStringUntil('\n').toInt();
  callib = true;
}
