'''
https://github.com/STEMinds/Eduponics-Mini
MIT License
Copyright (c) 2020 STEMinds

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Ph Buffer table:
|--------------------------------------------------------------------------------------------------|
| T(c) | Buffer 1.679 | Buffer 4.008 | Buffer 7.000 | Buffer 9.180 | Buffer 10.012 | Buffer 12.454 |
---------------------------------------------------------------------------------------------------|
|  5   |     1.668    |     3.998    |     7.087    |     9.395    |     10.245    |    13.207     |
|  10  |     1.670    |     3.997    |     7.059    |     9.332    |     10.179    |    13.003     |
|  15  |     1.672    |     3.998    |     7.036    |     9.276    |     10.118    |    12.810     |
|  20  |     1.675    |     4.001    |     7.016    |     9.226    |     10.062    |    12.627     |
|  25  |     1.679    |     4.005    |     7.000    |     9.180    |     10.012    |    12.454     |
|  30  |     1.683    |     4.011    |     6.987    |     9.139    |     9.966     |    12.289     |
|  35  |     1.688    |     4.018    |     6.977    |     9.102    |     9.925     |    12.289     |
|  40  |     1.694    |     4.027    |     6.970    |     9.068    |     9.889     |    12.133     |
|  45  |     1.700    |     4.038    |     6.966    |     9.038    |     9.856     |    11.984     |
|  50  |     1.707    |     4.050    |     6.964    |     9.010    |     9.828     |    11.795     |
----------------------------------------------------------------------------------------------------
'''

from ads1x15 import ADS1115
import mcp23017
from machine import I2C, Pin
import time

# IO12 reserved for powering the board, define it
power = Pin(12, Pin.OUT)
# activate the board
power.value(1)

# setup I2C
i2c = I2C(scl=Pin(33), sda=Pin(32))

# define MCP with MOSFET pins
mcp = mcp23017.MCP23017(i2c, 0x20)
# set pins to high (activate all MOSFETs)
mcp.pin(8, mode=0, value=0)
mcp.pin(9, mode=0, value=0)
mcp.pin(10, mode=0, value=0)
mcp.pin(11, mode=0, value=0)

# setup adc for the extension board
address = 0x48
gain = 1
adc = ADS1115(i2c, address, gain)

def read_ph():
    '''
    pH 4.0 and 7.0 values should be modified accordingly using the potentiometer
    '''
    # get voltage
    adc_read = adc.read(0)
    voltage = adc_read["voltage"]
    print("voltage: %s" % adc_read)
    # pH 4.0
    _acidVoltage = 3507
    # pH 7.0
    _neutralVoltage = 2990.5
    # calculate slope and intercept
    slope = (7.0-4.0)/((_neutralVoltage-1500.0) / 3.0 - (_acidVoltage-1500.0)/3.0)
    intercept = 7.0 - slope*(_neutralVoltage-1500.0)/3.0
    # get the pH value
    _phValue = slope*(voltage-1500.0)/3.0+intercept
    # return it
    return round(_phValue, 2)

while True:
    print("pH: %s" % read_ph())
    print("")
    time.sleep(0.5)
