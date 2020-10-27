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

#include <Adafruit_NeoPixel.h>

#define PIN 14

// When we setup the NeoPixel library, we tell it how many pixels, and which pin to use to send signals.
// Note that for older NeoPixel strips you might need to change the third parameter--see the strandtest
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(1, PIN, NEO_GRB + NEO_KHZ800);

void setup()
{
  pixels.begin(); // This initializes the NeoPixel library.
}

void loop()
{
  pixels.setPixelColor(0, pixels.Color(255, 0, 0)); // set to red, full brightness
  pixels.show(); // This sends the updated pixel color to the hardware.
  delay(1000);
  pixels.setPixelColor(0, pixels.Color(0, 255, 0)); // set to green, full brightness
  pixels.show(); // This sends the updated pixel color to the hardware.
  delay(1000);
  pixels.setPixelColor(0, pixels.Color(0, 0, 255)); // set to blue, full brightness
  pixels.show(); // This sends the updated pixel color to the hardware.
  delay(1000);
}
