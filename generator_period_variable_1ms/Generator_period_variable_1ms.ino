//GENERATOR_ADVANCED
//
//Generuje PWM zmienijący częstotliwość co 1 okres.
//Okres: 1ms-262ms
//Listę i kolejność okresów można edytować w zmiennej T_ms_tbl (ms).
//
//INPUT: 2-PD2(Uno), 2-PD1(Leonardo) 
//OUTPUT: 10-PB2(Uno), 10-PB6(Leonardo) (musi być podłączony do wejścia - pin 2)
//
//Program na każdym zboczu rosnącym PWM-a wyjściowego zmienia wartość w rejestrze na kolejną wartość z tablicy okresów, a co za tym idzie okres przsebiegu wyjściowego.

#define FEEDBACK_TIMEBASE_PIN 2

#define NR_OF_PERIODS 3

void TimerConfig(unsigned int T_ms){
  DDRB |= (1<<PB2); //alternatively pinMode(10, OUT);(PB2 - Uno, PB6 Leonardo) - setting pin connected to sqr_wave_gen direction to output
  TCCR1A |= (1<<WGM11)|(1<<WGM10); //COM1A0|WGM11|WGM10 - non inverting, fast PWM mode, TOP in OCR1A
  TCCR1A &= ~((1<<COM1A1)|(1<<COM1A0)|(1<<COM1B0)|(1<<COM1B1));
  TCCR1B |= (1<<WGM13)|(1<<WGM12)|(1<<CS11)|(1<<CS10); //WGM13|WGM12|CS10 - further setting timer mode and setting prescaler to 64
  TCCR1B &= ~((1<<ICNC1)|(1<<ICES1)|(1<<CS12));
  OCR1A = T_ms*250;//!!!setting TOP value for the counter to reset (f_timer = f_clk/(N*(1+TOP))) N = 1, f_clk = 16MHz
  OCR1B = OCR1A/2;
}

void TimerStart(){
  TCCR1A |= (1<<COM1B1);
}

byte T_ms_tbl[NR_OF_PERIODS];// = {4, 10, 40}; //tablica okresów w ms

byte tbl_iter = 0;

void OnChange_FeedbackTimebase(){
  OCR1A = T_ms_tbl[(tbl_iter++)%NR_OF_PERIODS]*250;
  OCR1B = OCR1A/2;
}

void setup() {
  pinMode(FEEDBACK_TIMEBASE_PIN, INPUT_PULLUP);
  
  Serial.begin(115200);
  Serial.setTimeout(-1);
  Serial.println("COM opened;Waiting for periods");

  for(byte i = 0; i<NR_OF_PERIODS;i++){
    T_ms_tbl[i] = Serial.readStringUntil('\n').toInt();
  }
  TimerConfig(T_ms_tbl[0]);
  attachInterrupt(digitalPinToInterrupt(FEEDBACK_TIMEBASE_PIN), OnChange_FeedbackTimebase, RISING);
  TimerStart();

  Serial.println("Started");
}

void loop() {}
