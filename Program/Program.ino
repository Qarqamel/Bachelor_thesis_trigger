//MEASURE_PERIOD
//
//Mierzy okres PWM-a wejściowego SAMPLE_NR razy i wysyła wyniki przez UART.
//Pomiar rozpoczyna się po odebraniu na UART-cie dowolnej wiadomości zakończonej terminatorem ('\n').
//Okres wejściowy: 0-32767us
//
//INPUT: 8-PB0(Uno), 4-PD4(Leonardo), 49-PL0(Mega)
//OUTPUT: -
//
//Program korzysta z funkcji input capture 16-bitowego timera timer1(Uno, Leonardo). Timer działa w trybie CTC(Uno, Leonardo) z preskalerem ustawionym na 8.
//Po otrzymaniu terminatora na UART-cie program rozpoczyna pomiar.
//Na zboczach rosnących przebiegu wejściowego, wpisuje czas od poprzedniego zbocza rsonącego, do tablicy wyników.
//Po wypełnieniu wysyła tablicę wyników przez UART.

#define SAMPLE_NR 400

#define ENABLE_INPUT_CAPTURE() (TIMSK1 |= (1<<ICIE1))
#define DISABLE_INPUT_CAPTURE() (TIMSK1 &= ~(1<<ICIE1))

uint16_t captured_times[SAMPLE_NR];
uint16_t captured_time_prev;
unsigned int sample_ctr = 0;
volatile bool acquisition_complete = false;

ISR(TIMER1_CAPT_vect){
  captured_times[sample_ctr++] = ICR1 - captured_time_prev; //poniewaz int an ATMEGA ma 16bitów - nie jest konieczna obsługa przekręcania licznika timera
  captured_time_prev = ICR1;
  if(sample_ctr == SAMPLE_NR){
    DISABLE_INPUT_CAPTURE();
    acquisition_complete = true;
  }
}

void setup() {

  pinMode(4, INPUT); //ICP1 pin - input capture pin. pin 4 - PD4 for Leonardo; pin 8 - PB0 for Uno
  TCCR1B = 0b01011010; //selecting edge for input capture, setting timer mode to CTC, and prescaler to 8
  
  Serial.begin(115200);
  Serial.setTimeout(-1);
}

void loop() {

  Serial.readStringUntil('\n');
  sample_ctr = 0;
  acquisition_complete = false;
  ENABLE_INPUT_CAPTURE();

  while(!acquisition_complete){}

  for(unsigned int i = 0; i < SAMPLE_NR; i++){
    Serial.println(captured_times[i]);
  }
}
