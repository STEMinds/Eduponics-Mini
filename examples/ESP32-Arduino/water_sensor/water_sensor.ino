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
  // if digital read is 0 means no water
  // if digital read is 1 means there is water
  if(is_empty()){
    Serial.println("The water container is empty");
  }else{
    Serial.println("The water container is full");
  }
  // wait 100 miliseconds and check again
  delay(100);
}
