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

import dht
import machine
import math
import neopixel
import time

def calculate_humidex(T,RH):
    # find dewpoint in celsius
    dewpoint_c = 243.04 * (math.log(RH/100,math.e)+((17.625*T)/(243.04+T)))/(17.625-math.log(RH/100,math.e)-((17.625*T)/(243.04+T)))
    # convert celsius to Kelvin
    dewpoint_k = (dewpoint_c + 273.15)
    # find the humidex using the dewpoint we found earlier
    humidex = T + (0.5555)*(6.11 * math.exp(5417.7530 * ((1/273.16) - (1/dewpoint_k))) - 10.0)
    # return  humidex
    return humidex

# initialize dht object, DHT11 coonected to IO19
d = dht.DHT11(machine.Pin(19))
# configure neopixel
np = neopixel.NeoPixel(machine.Pin(14), 1)

try:
    while True:
        # measure sensor data
        d.measure()
        # get temperature and humidity
        temperature = d.temperature()
        humidity = d.humidity()
        # get humidex
        humidex = calculate_humidex(temperature,humidity)

        # check the value of the humidex
        if(humidex > 0 and humidex < 29):
            # Turn on green RGB
            np[0] = (0, 255, 0) # set to green, full brightness
        if(humidex >= 30 and humidex <= 39):
            # Turn on yellow RGB
            np[0] = (255, 255, 0) # set to red, full brightness
        if(humidex > 40):
            # Turn on red RGB
            np[0] = (255, 0, 0) # set to red, full brightness

        # write the data to the RGB
        np.write()
        # print temperature and humidity
        print("--------------------------")
        print("temperature : %s" % temperature)
        print("humidity : %s" % humidity)
        print("humidex : %s" % humidex)
        print("--------------------------")
        print("")
        # sleep for 1 second
        time.sleep(1)
except KeyboardInterrupt:
    # keyboard interrupt, let's turn off LED
    np[0] = (0, 0, 0)
    np.write()
