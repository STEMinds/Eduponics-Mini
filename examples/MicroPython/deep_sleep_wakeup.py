"""
MicroPython deep sleep wakeup by button example
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
import esp32
import time

wake_up = machine.Pin(36, mode = machine.Pin.IN)

#level parameter can be: esp32.WAKEUP_ANY_HIGH or esp32.WAKEUP_ALL_LOW
esp32.wake_on_ext0(pin = wake_up, level = esp32.WAKEUP_ANY_HIGH)

#your main code goes here to perform a task

print('Im awake now. Going to sleep in 5 seconds ...')
time.sleep(5)
print('Going to sleep now ..')
machine.deepsleep()
