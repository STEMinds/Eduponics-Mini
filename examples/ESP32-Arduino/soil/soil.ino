#define soilMoisturePin 35

void setup() {
  Serial.begin(115200);
}

int value_in_percentage(int value){
  // set max val and min val of the sensor
  // this requires manual calibration
  // minVal get be recieved by putting the sensor submerged in the water
  // maxVal can be recieved by making sure the sensor is dry in the clear air
  float minVal = 710;
  float maxVal = 4095;
  //scale the value based on maxVal and minVal
  float scale = 100.00 / (minVal - maxVal);
  //get calculated scale
  int normal_reading = (value - maxVal) * scale;
  // we can also get inverted value if needed
  int inverted_reading = (minVal - value) * scale;
  // for this example we'll return only the normal reading
  return normal_reading;
}

void loop() {
  int value = analogRead(soilMoisturePin);
  int estimated = value_in_percentage(value);
  // print sensor analog value
  Serial.print("Sensor value: ");
  Serial.print(value);
  // print sensor value in precentage
  Serial.print("Sensor value in precentage: ");
  Serial.print(estimated);
  Serial.println("%");

  delay(1000);
}
