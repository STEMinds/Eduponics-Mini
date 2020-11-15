from ads1x15 import ADS1115
from machine import I2C, Pin
import time

# setup I2C
i2c = I2C(scl=Pin(33), sda=Pin(32))

class SoilMoisture():

    def __init__(self,i,i2c):
        # get parameters
        self.i2c = i2c
        self.address = 0x48
        self.gain = 1
        self.sensor = i
        # establish adc
        self.adc = ADS1115(self.i2c, self.address, self.gain)

    def read(self):
        raw = self.adc.read(4,self.sensor,None)
        voltage = self.adc.raw_to_v(raw)
        # check if sensor connected based on voltage
        if(round(voltage,2) == 0.56):
            state = False
        else:
            state = True
            voltage = voltage - 0.558
        return {"raw":raw,"voltage":voltage, "connected":state}

soil_1 = SoilMoisture(0,i2c)
soil_2 = SoilMoisture(1,i2c)
soil_3 = SoilMoisture(2,i2c)
soil_4 = SoilMoisture(4,i2c)

while True:
    print("Soil moisture 1: %s " % soil_1.read())
    print("Soil moisture 2: %s " % soil_2.read())
    print("Soil moisture 3: %s " % soil_3.read())
    print("Soil moisture 4: %s " % soil_4.read())
    time.sleep(1)
