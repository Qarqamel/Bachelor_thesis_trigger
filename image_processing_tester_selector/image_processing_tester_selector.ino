#define PULSE_PIN 5

void Pulse(byte pin_nr){
  digitalWrite(pin_nr, HIGH);
  delay(10);
  digitalWrite(pin_nr, LOW);
}

void setup() {
  pinMode(PULSE_PIN, OUTPUT);

  Serial.begin(115200);
  Serial.setTimeout(-1);
  Serial.println("Started");
}

void loop() {
  Serial.readStringUntil('\n');
  Pulse(PULSE_PIN);
}
