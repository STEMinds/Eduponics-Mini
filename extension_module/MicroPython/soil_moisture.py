from ads1x15 import ADS1115
from machine import I2C, Pin
import time

# setup I2C
i2c = I2C(scl=Pin(33), sda=Pin(32))
# setup adc
address = 0x48
gain = 1
adc = ADS1115(i2c, address, gain)

while True:
    print("Soil moisture 1: %s " % adc.read(0))
    print("Soil moisture 2: %s " % adc.read(1))
    print("Soil moisture 3: %s " % adc.read(2))
    print("Soil moisture 4: %s " % adc.read(3))
    time.sleep(1)
