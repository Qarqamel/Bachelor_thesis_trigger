//GENERATOR
//
//Generuje PWM o zadanym okresie(ms).
//Okres: 1ms-262ms
//Okres podawany przez UART (wysłanie liczby całkowitej dodatniej z terminatorem ('/n')).
//
//INPUT: -
//OUTPUT: 10-PB2(Uno), 10-PB6(Leonardo)
//
//Przy użyciu 16-bitowego timera (timer1) pracującego w trybie non inverting fast PWM z prescalerem 64, generuje przebieg prostkątny. 
//Okres przebiegu przyjmowany jest przez UART-a, następnie zwracany spowrotem i wpisywany do rejestru Output compare timera, w celu zmiany okresu przebiego.

void TimerConfig(unsigned int T_ms){
  DDRB |= (1<<PB2); //alternatively pinMode(10, OUT);(PB2 - Uno, PB6 Leonardo) - setting pin connected to sqr_wave_gen direction to output
  TCCR1A |= (1<<WGM11)|(1<<WGM10)|(1<<COM1B1); //WGM11|WGM10 - non inverting, fast PWM mode, TOP in OCR1A
  TCCR1A &= ~((1<<COM1A1)|(1<<COM1A0)|(1<<COM1B0));
  TCCR1B |= (1<<WGM13)|(1<<WGM12)|(1<<CS11)|(1<<CS10); //WGM13|WGM12|CS10 - further setting timer mode and setting prescaler to 64
  TCCR1B &= ~((1<<ICNC1)|(1<<ICES1)|(1<<CS12));
  OCR1A = T_ms*250;//setting TOP value for the counter to reset (f_timer = f_clk/(N*(1+TOP))) N = 1, f_clk = 16MHz
  OCR1B = OCR1A/2;
}

void setup() {
  
  Serial.begin(115200);
  Serial.setTimeout(-1);
  Serial.println("COM opened;Waiting for period");
}

void loop() {
  // put your main code here, to run repeatedly:
  unsigned int T_ms = Serial.readStringUntil('\n').toInt();
  TimerConfig(T_ms);
  Serial.println("Period set;Send period to adj");
}
