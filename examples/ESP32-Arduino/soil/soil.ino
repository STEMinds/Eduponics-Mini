// Arduino IDE BH1750 Eduponics Mini Example
// https://github.com/STEMinds/eduponics-mini
//
// MIT License
// Copyright (c) 2020 STEMinds
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

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
