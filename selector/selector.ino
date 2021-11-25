//MAIN
//
//Nalicza counter na zboczach PWM-a wejściowego, równocześnie przyjmując przez UART-a timestampy oraz porównując je z counterem.
//
//INPUT: 2-PD2(Uno), 2-PD1(Leonardo)
//OUTPUT: -
//
//Zbocza rosnące generują przerwania, w których counter jest inkrementowany. 
//W pętli głównej program przyjmuje prz UART-a timestampy, wpisuje je do tablicy i sprawdza, czy nie są mniejsze od countera.
//Jeśli tak, to usuwa je z tablicy i zwraca informację przez UART.
//#include <arduino-timer.h>

#define SR_SYNC                   1

#define MAX_TSTAMP_NR             10

#define WAIT_TO_START_PIN         11
#define STARTED_PIN               13
#define SELECT_PULSE_PIN          5
#define TIMEBASE_PIN              2
#define TMSTMP_OVERFLOW_LED_PIN   7

void StartupSynchronization(){
  pinMode(WAIT_TO_START_PIN, INPUT_PULLUP);
  pinMode(STARTED_PIN, INPUT_PULLUP);
  while(digitalRead(WAIT_TO_START_PIN)){}
  pinMode(STARTED_PIN, OUTPUT);
  digitalWrite(STARTED_PIN, 0);
}

struct Timestamp{
  bool valid;
  unsigned int uiValue;
  };

volatile unsigned long time_base_ctr = 0;

void OnChange_Timebase(){
  time_base_ctr++;
}

void Pulse(byte pin_nr){
  digitalWrite(pin_nr, HIGH);
  delay(10);
  digitalWrite(pin_nr, LOW);
}

void setup() {  
  pinMode(SELECT_PULSE_PIN, OUTPUT);
  pinMode(TMSTMP_OVERFLOW_LED_PIN, OUTPUT);
  pinMode(TIMEBASE_PIN, INPUT_PULLUP);
  
  Serial.begin(115200); 
  Serial.setTimeout(0);
  Serial.println("Init");

  if (!SR_SYNC){
    StartupSynchronization();
  }   
  attachInterrupt(digitalPinToInterrupt(TIMEBASE_PIN), OnChange_Timebase, RISING);
  if (SR_SYNC){
    Serial.println("Started");
  }
}



void loop() {
  
  static struct Timestamp tstamps[MAX_TSTAMP_NR];
  static bool new_tstamp_flag = false;
  static char serial_buffer[20];
  static byte char_ctr=0;
  
  // tstamps reception
  // from serial
  while (Serial.available()){
     char c = Serial.read();   
     serial_buffer[char_ctr++]=c;
     if (c == '\n') {
        serial_buffer[char_ctr] = 0;      
        char_ctr = 0;
        new_tstamp_flag = true;
        break;      
     }
  }
  
  // to table
  if (new_tstamp_flag){
     new_tstamp_flag = false;
     byte i;
     for(i = 0; i < MAX_TSTAMP_NR; i++){      
        if(tstamps[i].valid == false){
           tstamps[i].valid = true;
           tstamps[i].uiValue = atoi(serial_buffer);          
           break;
        }
     }
     if(i==MAX_TSTAMP_NR){
        digitalWrite(TMSTMP_OVERFLOW_LED_PIN, HIGH);
     }
  }

  // tstamps expirity check
  for(byte i = 0; i < MAX_TSTAMP_NR; i++){      
     if(tstamps[i].valid){
        if(tstamps[i].uiValue <= time_base_ctr){
           tstamps[i].valid = false;
           Pulse(SELECT_PULSE_PIN);
           break;        
        }
     }
  }
}
