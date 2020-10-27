"""
MicroPython 12V Pump using relay example
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

import machine
import time

# define pump on pin IO23 as OUTPUT
pump = machine.Pin(23, machine.Pin.OUT)
# define water quantity, 0 when full 1 when empty
water_quantity = machine.Pin(21, machine.Pin.IN)

def is_empty():
    return water_quantity.value()

# define pump on pin IO23 as OUTPUT
pump = machine.Pin(23, machine.Pin.OUT)
# turn on the pump
pump.value(1)
while not is_empty():
    # not empty yet, keep giving water
    time.sleep(0.1)

# oh no, now the bucket is empty, stop it!
# turn off the pump
pump.value(0)
