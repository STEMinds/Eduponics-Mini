"""
MicroPython Soil moisture sensor example
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

from machine import ADC,Pin
import neopixel
import time

# set max val and min val of the sensor
# this requires manual calibration
# minVal get be recieved by putting the sensor submerged in the water
# maxVal can be recieved by making sure the sensor is dry in the clear air
minVal = 710
maxVal = 4095
# configure neopixel
np = neopixel.NeoPixel(Pin(14), 1)

def value_in_percentage(val):
    # scale the value based on maxVal and minVal
    scale = 100 / (minVal - maxVal)
    # get calculated scale
    normal_reading = ("%s%s" % (int((val - maxVal) * scale),"%"))
    # we can also get inverted value if needed
    inverted_reading = ("%s%s" % (int((minVal - val) * scale),"%"))
    # for this example we'll return only the normal reading
    return normal_reading

# set adc (analog to digital) on pin 35
adc = ADC(Pin(35))
# read analog input
adc.read()
# set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
adc.atten(ADC.ATTN_11DB)

# keep running the software till we stop it manually.
try:
    while True:
        # get sensor value
        value = adc.read()
        # get the value in percentage, convert it to int
        estimated = int(value_in_percentage(value).replace("%",""))
        if(estimated >= 0 and estimated < 35):
            # turn RED color, it's critical
            np[0] = (255, 0, 0) # set to red, full brightness
        if(estimated >= 35 and estimated < 65):
            # turn YELLOW color, it's alright for now
            np[0] = (255, 255, 0) # set to yellow, full brightness
        if(estimated >= 65 and estimated <= 100):
            # turn GREEN color, we have enough water
            np[0] = (0, 255, 0) # set to green, full brightness
        # write changes of the RGB LED color
        np.write()
        # print the analog results (moisture)
        print("sensor value: %s" % value)
        print("sensor value in percentage: %s" % value_in_percentage(value))
        # sleep for 1 second
        time.sleep(1)
except KeyboardInterrupt:
    # keyboard interrupt, let's turn off LED
    np[0] = (0, 0, 0)
    np.write()
