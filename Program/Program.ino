//METER_ADVANCED
//
//Mierzy czas(us) od resetu na zboczach PWM-a wejściowego SAMPLE_NR razy i wysyła wyniki przez UART.
//Pomiar rozpoczyna się po odebraniu na UART-cie dowolnej wiadomości zakończonej terminatorem ('\n').
//Okres wejściowy: 0-4294967295us
//
//INPUT: 2-PD2(Uno), 2-PD1(Leonardo)
//OUTPUT: -
//
//Po otrzymaniu terminatora na UART-cie program rozpoczyna pomiar, na zboczach rosnących przebiegu wejściowego wpisując czas od resetu do tablicy wyników. 
//Po wypełnieniu wysyła tablicę wyników przez UART.

#define SAMPLE_NR 400

unsigned long times[SAMPLE_NR];
unsigned int times_iter = 0;
volatile bool acquisition_complete = false;

void Interrupt_routine(){
  times[times_iter++] = micros();
  if(times_iter == SAMPLE_NR){
    detachInterrupt(digitalPinToInterrupt(2));
    acquisition_complete = true;
  }
}

void setup() {

  Serial.begin(115200);
  Serial.setTimeout(-1);

  pinMode(2, INPUT);
  }

void loop() {
  Serial.readStringUntil('\n');
  times_iter = 0;
  acquisition_complete = false;  
  attachInterrupt(digitalPinToInterrupt(2), Interrupt_routine, RISING);

  while(!acquisition_complete){}
  
  for(unsigned int i = 0; i < SAMPLE_NR; i++){
    Serial.println(times[i]);
  }
}
