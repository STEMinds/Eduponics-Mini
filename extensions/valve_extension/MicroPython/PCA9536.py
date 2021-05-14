"""
MicroPython DHT11 sensor example
https://github.com/STEMinds/eduponics-mini
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
"""

from machine import I2C, Pin
import time

# define the PCA9536 IO extender pins
PCA9536_I2C_ADDRESS         = 0x41

PCA9536_REG_OUTPUT_PORT     = 0x01
PCA9536_REG_POL_INVERSION   = 0x02
PCA9536_REG_CONFIG          = 0x03

PCA9536_CONF_OUTPUT         = 0x00
PCA9536_ALL_OUTPUTS_OFF     = 0x00
PCA9536_PIN0_OUTPUT         = 0x00
PCA9536_PIN1_OUTPUT         = 0x00
PCA9536_PIN2_OUTPUT         = 0x00
PCA9536_PIN3_OUTPUT         = 0x00

# define 4 valve channel with their registers
valve_case = {
    0:0x03,
    1:0x05,
    2:0x07,
    3:0x09
}

class Valve():

    def __init__(self, i2c):

		# initalize valve with I2C and address
        self.i2c = i2c
        self.address = PCA9536_I2C_ADDRESS
        self.register = PCA9536_REG_OUTPUT_PORT

		# create bytes array
        self.barray = bytearray(1)
        self.barray[0] = 0x00

		# turn off all the relays on initalize
        self.i2c.writeto_mem(self.address,PCA9536_REG_OUTPUT_PORT,  self.barray)
        self.i2c.writeto_mem(self.address,PCA9536_REG_CONFIG, self.barray)

    def write(self, channel=0, state=0):

		# convert ID (0-3) to register address
		if(channel in valve_case):
        	channel = valve_case[channel]
		else:
			print("[!] The relay only has 4 channels! (0-3)")
			return 0

        if(state):
            state &= ~(1 << state|channel)
            self.barray[0] = state
            print(self.barray)
            self.i2c.writeto_mem(self.address, self.register, self.barray)
        else:
            state |= (state | channel)
            self.barray[0] = state
            print(self.barray)
            self.i2c.writeto_mem(self.address, self.register, self.barray)
