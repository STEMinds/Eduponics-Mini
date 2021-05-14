// I2C device class (I2Cdev) demonstration Arduino sketch for ADS1115 class
// Example of reading two differential inputs of the ADS1115 and showing the value in mV
// 2016-03-22 by Eadf (https://github.com/eadf)
// Updates should (hopefully) always be available at https://github.com/jrowberg/i2cdevlib
//
// Changelog:
//     2016-03-22 - initial release

/* ============================================
I2Cdev device library code is placed under the MIT license
Copyright (c) 2011 Jeff Rowberg
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
===============================================
Wiring the ADS1115 Module to an Arduino UNO
ADS1115 -->  UNO
  VDD        5V
  GND        GND
  SCL        A5 (or SCL)
  SDA        A4 (or SDA)
  ALRT       2
*/

#include "ADS1115.h"
#include <MCP23017.h>

ADS1115 adc0(0x48);

#define MCP23017_ADDR 0x20
MCP23017 mcp = MCP23017(MCP23017_ADDR);

// Wire ADS1115 ALERT/RDY pin to pin 25
const int alertReadyPin = 25;

void setup() {
    //I2Cdev::begin();  // join I2C bus
    Wire.begin(33,32);
    Serial.begin(115200); // initialize serial communication

    Serial.println("Testing device connections...");
    Serial.println(adc0.testConnection() ? "ADS1115 connection successful" : "ADS1115 connection failed");

    adc0.initialize(); // initialize ADS1115 16 bit A/D chip

    // We're going to do single shot sampling
    adc0.setMode(ADS1115_MODE_SINGLESHOT);

    // Slow things down so that we can see that the "poll for conversion" code works
    adc0.setRate(ADS1115_RATE_8);

    // Set the gain (PGA) +/- 4.096V
    // Note that any analog input must be higher than –0.3V and less than VDD +0.3
    adc0.setGain(ADS1115_PGA_4P096);
    // ALERT/RDY pin will indicate when conversion is ready

    pinMode(alertReadyPin,INPUT_PULLUP);
    adc0.setConversionReadyPinMode();

    // To get output from this method, you'll need to turn on the
    //#define ADS1115_SERIAL_DEBUG // in the ADS1115.h file
    #ifdef ADS1115_SERIAL_DEBUG
    adc0.showConfigRegister();
    Serial.print("HighThreshold="); Serial.println(adc0.getHighThreshold(),BIN);
    Serial.print("LowThreshold="); Serial.println(adc0.getLowThreshold(),BIN);
    #endif

    // init MCP unit
    mcp.init();

    mcp.portMode(MCP23017Port::I, 0); //Port A as output
    mcp.portMode(MCP23017Port::J, 0); //Port B as output
    mcp.portMode(MCP23017Port::K, 0); //Port C as output
    mcp.portMode(MCP23017Port::L, 0); //Port D as output

    mcp.writeRegister(MCP23017Register::GPIO_I, 0x00);  //Reset port A
    mcp.writeRegister(MCP23017Register::GPIO_J, 0x00);  //Reset port B
    mcp.writeRegister(MCP23017Register::GPIO_K, 0x00);  //Reset port C
    mcp.writeRegister(MCP23017Register::GPIO_L, 0x00);  //Reset port D
}

/** Poll the assigned pin for conversion status
 */
void pollAlertReadyPin() {
  for (uint32_t i = 0; i<100000; i++)
    if (!digitalRead(alertReadyPin)) return;
   Serial.println("Failed to wait for AlertReadyPin, it's stuck high!");
}

void loop() {

    // The below method sets the mux and gets a reading.
    adc0.setMultiplexer(ADS1115_MUX_P0_NG);
    adc0.triggerConversion();
    pollAlertReadyPin();
    Serial.print("A0: "); Serial.print(adc0.getMilliVolts(false)); Serial.print("mV\t");

    adc0.setMultiplexer(ADS1115_MUX_P1_NG);
    adc0.triggerConversion();
    pollAlertReadyPin();
    Serial.print("A1: "); Serial.print(adc0.getMilliVolts(false)); Serial.print("mV\t");

    adc0.setMultiplexer(ADS1115_MUX_P2_NG);
    adc0.triggerConversion();
    pollAlertReadyPin();
    Serial.print("A2: "); Serial.print(adc0.getMilliVolts(false)); Serial.print("mV\t");

    adc0.setMultiplexer(ADS1115_MUX_P3_NG);
    // Do conversion polling via I2C on this last reading:
    Serial.print("A3: "); Serial.print(adc0.getMilliVolts(true)); Serial.print("mV");

    Serial.println(digitalRead(alertReadyPin));
    delay(500);
}
