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
