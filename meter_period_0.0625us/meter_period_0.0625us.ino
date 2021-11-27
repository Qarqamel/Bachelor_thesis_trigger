//MEASURE_PERIOD
//
//Mierzy okres PWM-a wejściowego SAMPLE_NR razy i wysyła wyniki przez UART.
//Pomiar rozpoczyna się po odebraniu na UART-cie dowolnej wiadomości zakończonej terminatorem ('\n').
//Okres wejściowy: 0-32767us
//
//INPUT: 8-PB0(Uno), 4-PD4(Leonardo), 49-PL0(Mega)
//OUTPUT: -
//
//Program korzysta z funkcji input capture 16-bitowego timera (timer4(Mega)). Timer działa w trybie defaultowym - mode 0 (Mega) z preskalerem ustawionym na 1.
//Po otrzymaniu terminatora na UART-cie program rozpoczyna pomiar.
//Na zboczach rosnących przebiegu wejściowego, wpisuje czas od poprzedniego zbocza rsonącego, do tablicy wyników.
//Po wypełnieniu wysyła tablicę wyników przez UART.

#define TIMEBASE_PIN 49

#define SAMPLE_NR 2900
#define ENABLE_INPUT_CAPTURE() (TIMSK4 |= (1<<ICIE4))
#define DISABLE_INPUT_CAPTURE() (TIMSK4 &= ~(1<<ICIE4))

void TimerConfig(){
  //ICES - input capture edge select to rising, CS - setting prescaler to 1
  //WGM - setting waveform generation mode to 0
  TCCR4B |= (1<<ICES4)|(1<<CS40);
  TCCR4B &= ~((1<<ICNC4)|(1<<WGM43)|(1<<WGM42)|(1<<CS42)|(1<<CS41));
  TCCR4A &= ~((1<<COM4A1)|(1<<COM4A0)|(1<<COM4B1)|(1<<COM4B0)|(1<<COM4C1)|(1<<COM4C0)|(1<<WGM41)|(1<<WGM40));  
}

volatile unsigned int Periods[SAMPLE_NR];
volatile unsigned int Period_prev;

volatile unsigned int edge_ctr;
volatile bool acquisition_complete;
volatile bool first_acq;

ISR(TIMER4_CAPT_vect){

  if(first_acq){
    first_acq = false;
    Period_prev = ICR4;
    return;
  }
  Periods[edge_ctr++] = ICR4 - Period_prev;
  Period_prev = ICR4;
  if(edge_ctr == SAMPLE_NR){
    DISABLE_INPUT_CAPTURE();
    acquisition_complete = true;
  }
}

void setup() {
  pinMode(TIMEBASE_PIN, INPUT_PULLUP); //ICP1 pin - input capture pin. pin 4 - PD4 for Leonardo; pin 8 - PB0 for Uno;ICP4 pin 49 - PL1 for Mega
  
  Serial.begin(115200);
  Serial.setTimeout(-1);
  Serial.println("COM opened");

  TimerConfig();
  Serial.println("Started;Waiting for acq");
}

void loop() {
  Serial.readStringUntil('\n');
  acquisition_complete=false;
  edge_ctr=0;
  first_acq = true;
  ENABLE_INPUT_CAPTURE();

  while(!acquisition_complete){}

  for(unsigned int i=0; i<SAMPLE_NR; i++){
    Serial.println(Periods[i]);
  }
}
