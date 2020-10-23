// set the water sensor on IO pin number 21
const int water_sensor = 21;

void setup() {
  Serial.begin(115200);
  // configure pump as output
  pinMode(water_sensor, INPUT);
}

int is_empty(){
  return digitalRead(water_sensor);
}

void loop() {
  // when pump on low the relay is closed, no water is going through
  if(is_empty()){
    Serial.println("The water container is empty"); 
  }else{
    Serial.println("The water container is full"); 
  }
  // wait 100 miliseconds and check again
  delay(100);
}
