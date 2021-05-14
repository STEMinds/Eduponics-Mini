from ads1x15 import ADS1115
from machine import I2C, Pin
import mcp23017
import time

# IO12 reserved for powering the board, define it
power = Pin(12, Pin.OUT)
# activate the board
power.value(1)

# setup I2C
i2c = I2C(scl=Pin(33), sda=Pin(32))

# define MCP with MOSFET pins
mcp = mcp23017.MCP23017(i2c, 0x20)
# set pins to low (activate all MOSFETs)
mcp.pin(8, mode=0, value=0)
mcp.pin(9, mode=0, value=0)
mcp.pin(10, mode=0, value=0)
mcp.pin(11, mode=0, value=0)

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
