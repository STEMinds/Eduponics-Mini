"""
MicroPython water indication with RGB NeoPixel Example
https://github.com/STEMinds/eduponics-mini-upython
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

import machine, neopixel
import time

# define water level sensor as INPUT on IO pin number 21
water_level = machine.Pin(21, machine.Pin.IN)
# Configure the RGB LED at IO pin 14 (1 indicates 1 LED)
np = neopixel.NeoPixel(machine.Pin(14), 1)

def is_empty():
    # will return 0 if container have no water and 1 if it has water
    return water_level.value()

try:
    while True:
        if(is_empty()):
            print("[-] You don't have water in the container")
            np[0] = (255, 0, 0) # set to red, full brightness
        else:
            print("[-] The water container has sufficient amount of water")
            np[0] = (0, 255, 0) # set to green, full brightness
        # save changes
        np.write() # save changes
        # wait one second before checking again
        time.sleep(1)
except KeyboardInterrupt:
    # keyboard interrupt, let's turn off LED
    np[0] = (0, 0, 0)
    np.write()
