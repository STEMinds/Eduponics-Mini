"""
MicroPython TinyRTC I2C Module, DS1307 RTC + AT24C32N EEPROM
https://github.com/mcauser/micropython-tinyrtc
MIT License
Copyright (c) 2018 Mike Causer
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

# AT24C32A, 32K (32768 kbit / 4 KB), 128 pages, 32 bytes per page, i2c addr 0x50
import machine
import time

class AT24C32N(object):
    """Driver for the AT24C32N 32K EEPROM."""

    def __init__(self, i2c, i2c_addr=0x50, pages=128, bpp=32):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.pages = pages
        self.bpp = bpp # bytes per page

    def capacity(self):
        """Storage capacity in bytes"""
        return self.pages * self.bpp

    def read(self, addr, nbytes):
        """Read one or more bytes from the EEPROM starting from a specific address"""
        return self.i2c.readfrom_mem(self.i2c_addr, addr, nbytes, addrsize=16)

    def write(self, addr, buf):
        """Write one or more bytes to the EEPROM starting from a specific address"""
        offset = addr % self.bpp
        partial = 0
        # partial page write
        if offset > 0:
            partial = self.bpp - offset
            self.i2c.writeto_mem(self.i2c_addr, addr, buf[0:partial], addrsize=16)
            time.sleep_ms(5)
            addr += partial
        # full page write
        for i in range(partial, len(buf), self.bpp):
            self.i2c.writeto_mem(self.i2c_addr, addr+i-partial, buf[i:i+self.bpp], addrsize=16)
            time.sleep_ms(5)

i2c = machine.I2C(scl=machine.Pin(15), sda=machine.Pin(4))
eeprom = AT24C32N(i2c)
print(eeprom.read(0, 32))
eeprom.write(0, 'hello world')
print(eeprom.read(0, 11))
