from machine import Pin, I2C
import mcp23017
import time

i2c = I2C(scl=Pin(33), sda=Pin(32))

mcp = mcp23017.MCP23017(i2c, 0x20)

# set pins to low
mcp.pin(0, mode=0, value=0)
mcp.pin(1, mode=0, value=0)
mcp.pin(2, mode=0, value=0)
mcp.pin(3, mode=0, value=0)

# open relays
print("Turn on relays")
mcp[0].output(1)
time.sleep(0.5)
mcp[1].output(1)
time.sleep(0.5)
mcp[2].output(1)
time.sleep(0.5)
mcp[3].output(1)
time.sleep(0.5)

# close relays
print("Turn off relays")
mcp[0].output(0)
time.sleep(0.5)
mcp[1].output(0)
time.sleep(0.5)
mcp[2].output(0)
time.sleep(0.5)
mcp[3].output(0)
