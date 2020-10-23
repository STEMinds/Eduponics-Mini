#include <Wire.h>
#include <BH1750.h>

BH1750 lightMeter(0x5C);


void setup(){
  // start serial communication
  Serial.begin(115200);
  // start I2C on pins 4 and 15
  Wire.begin(4,15);
  // initialize the bh1750
  lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE, 0x5C, &Wire);
}


void loop() {

  float lux = lightMeter.readLightLevel();
  Serial.print("Light: ");
  Serial.print(lux);
  Serial.println(" lx");
  delay(3000);

}
