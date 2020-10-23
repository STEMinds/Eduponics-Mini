// set the pump on IO pin number 23
const int pump = 23;

void setup() {
  Serial.begin(115200);
  // configure pump as output
  pinMode(pump, OUTPUT);
}

void loop() {
  // when pump on low the relay is closed, no water is going through
  digitalWrite(pump, LOW);
  Serial.println("Relay is closed");
  delay(1000); 
  // if the pump is high, the relay is open, the water goes through
  digitalWrite(pump, HIGH);
  Serial.println("Relay is open");
  delay(1000);
}
