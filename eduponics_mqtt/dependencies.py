"""
MicroPython TinyRTC I2C Module, DS1307 RTC + AT24C32N EEPROM
https://github.com/mcauser/micropython-tinyrtc
MIT License
Copyright (c) 2018 Mike Causer

MicroPython BH1750 light sensor module
https://github.com/STEMinds/eduponics-mini
MIT License
Copyright (c) 2020 STEMinds

BME280 Library Final Document: BST-BME280-DS002-15
Authors: Paul Cunnane 2016, Peter Dahlebrg 2016
Module borrows from the Adafruit BME280 Python library. Original Copyright notices are reproduced below.
Those libraries were written for the Raspberry Pi.
Copyright (c) 2014 Adafruit Industries
Author: Tony DiCola
Based on the BMP280 driver with BME280 changes provided by
David J Taylor, Edinburgh (www.satsignal.eu)
Based on Adafruit_I2C.py created by Kevin Townsend.

ADS1X15 Copyright (c) 2016 Radomir Dopieralski (@deshipu), 2017 Robert Hammelrath (@robert-hh)

MicroPython MCP23017 16-bit I/O Expander
https://github.com/mcauser/micropython-mcp23017
MIT License
Copyright (c) 2019 Mike Causer

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
from ustruct import unpack
from array import array
from micropython import const
import utime as time

_REGISTER_CONVERT = const(0x00)
_REGISTER_CONFIG = const(0x01)
_REGISTER_LOWTHRESH = const(0x02)
_REGISTER_HITHRESH = const(0x03)

_OS_SINGLE = const(0x8000)  # Write: Set to start a single-conversion
_OS_NOTBUSY = const(0x8000)  # Read: Bit=1 when no conversion is in progress

_MUX_DIFF_0_1 = const(0x0000)  # Differential P  =  AIN0, N  =  AIN1 (default)
_MUX_DIFF_0_3 = const(0x1000)  # Differential P  =  AIN0, N  =  AIN3
_MUX_DIFF_1_3 = const(0x2000)  # Differential P  =  AIN1, N  =  AIN3
_MUX_DIFF_2_3 = const(0x3000)  # Differential P  =  AIN2, N  =  AIN3
_MUX_SINGLE_0 = const(0x4000)  # Single-ended AIN0
_MUX_SINGLE_1 = const(0x5000)  # Single-ended AIN1
_MUX_SINGLE_2 = const(0x6000)  # Single-ended AIN2
_MUX_SINGLE_3 = const(0x7000)  # Single-ended AIN3

_PGA_6_144V = const(0x0000)  # +/-6.144V range  =  Gain 2/3
_PGA_4_096V = const(0x0200)  # +/-4.096V range  =  Gain 1
_PGA_2_048V = const(0x0400)  # +/-2.048V range  =  Gain 2 (default)
_PGA_1_024V = const(0x0600)  # +/-1.024V range  =  Gain 4
_PGA_0_512V = const(0x0800)  # +/-0.512V range  =  Gain 8
_PGA_0_256V = const(0x0A00)  # +/-0.256V range  =  Gain 16

_MODE_CONTIN = const(0x0000)  # Continuous conversion mode
_MODE_SINGLE = const(0x0100)  # Power-down single-shot mode (default)

_DR_128SPS = const(0x0000)   # 128 /8 samples per second
_DR_250SPS = const(0x0020)   # 250 /16 samples per second
_DR_490SPS = const(0x0040)   # 490 /32 samples per second
_DR_920SPS = const(0x0060)   # 920 /64 samples per second
_DR_1600SPS = const(0x0080)  # 1600/128 samples per second (default)
_DR_2400SPS = const(0x00A0)  # 2400/250 samples per second
_DR_3300SPS = const(0x00C0)  # 3300/475 samples per second
_DR_860SPS = const(0x00E0)  # -   /860 samples per Second

_CMODE_TRAD = const(0x0000)  # Traditional comparator with hysteresis (default)

_CPOL_ACTVLOW = const(0x0000)  # ALERT/RDY pin is low when active (default)

_CLAT_NONLAT = const(0x0000)  # Non-latching comparator (default)
_CLAT_LATCH = const(0x0004)  # Latching comparator

_CQUE_1CONV = const(0x0000)  # Assert ALERT/RDY after one conversions
# Disable the comparator and put ALERT/RDY in high state (default)
_CQUE_NONE = const(0x0003)

_GAINS = (
    _PGA_6_144V,  # 2/3x
    _PGA_4_096V,  # 1x
    _PGA_2_048V,  # 2x
    _PGA_1_024V,  # 4x
    _PGA_0_512V,  # 8x
    _PGA_0_256V   # 16x
)

_GAINS_V = (
    6.144,  # 2/3x
    4.096,  # 1x
    2.048,  # 2x
    1.024,  # 4x
    0.512,  # 8x
    0.256  # 16x
)

_CHANNELS = {
    (0, None): _MUX_SINGLE_0,
    (1, None): _MUX_SINGLE_1,
    (2, None): _MUX_SINGLE_2,
    (3, None): _MUX_SINGLE_3,
    (0, 1): _MUX_DIFF_0_1,
    (0, 3): _MUX_DIFF_0_3,
    (1, 3): _MUX_DIFF_1_3,
    (2, 3): _MUX_DIFF_2_3,
}

_RATES = (
    _DR_128SPS,   # 128/8 samples per second
    _DR_250SPS,   # 250/16 samples per second
    _DR_490SPS,   # 490/32 samples per second
    _DR_920SPS,   # 920/64 samples per second
    _DR_1600SPS,  # 1600/128 samples per second (default)
    _DR_2400SPS,  # 2400/250 samples per second
    _DR_3300SPS,  # 3300/475 samples per second
    _DR_860SPS    # - /860 samples per Second
)


class ADS1115:
    def __init__(self, i2c, address=0x48, gain=1):
        self.i2c = i2c
        self.address = address
        self.gain = gain
        self.temp2 = bytearray(2)

    def _write_register(self, register, value):
        self.temp2[0] = value >> 8
        self.temp2[1] = value & 0xff
        self.i2c.writeto_mem(self.address, register, self.temp2)

    def _read_register(self, register):
        self.i2c.readfrom_mem_into(self.address, register, self.temp2)
        return (self.temp2[0] << 8) | self.temp2[1]

    def raw_to_v(self, raw):
        v_p_b = _GAINS_V[self.gain] / 32767
        return raw * v_p_b

    def set_conv(self, rate=4, channel1=0, channel2=None):
        """Set mode for read_rev"""
        self.mode = (_CQUE_NONE | _CLAT_NONLAT |
                     _CPOL_ACTVLOW | _CMODE_TRAD | _RATES[rate] |
                     _MODE_SINGLE | _OS_SINGLE | _GAINS[self.gain] |
                     _CHANNELS[(channel1, channel2)])

    def read_raw(self, rate=4, channel1=0, channel2=None):
        """Read voltage between a channel and GND.
           Time depends on conversion rate."""
        self._write_register(_REGISTER_CONFIG, (_CQUE_NONE | _CLAT_NONLAT |
                             _CPOL_ACTVLOW | _CMODE_TRAD | _RATES[rate] |
                             _MODE_SINGLE | _OS_SINGLE | _GAINS[self.gain] |
                             _CHANNELS[(channel1, channel2)]))
        while not self._read_register(_REGISTER_CONFIG) & _OS_NOTBUSY:
            time.sleep_ms(1)
        res = self._read_register(_REGISTER_CONVERT)
        return res if res < 32768 else res - 65536

    def read_rev(self):
        """Read voltage between a channel and GND. and then start
           the next conversion."""
        res = self._read_register(_REGISTER_CONVERT)
        self._write_register(_REGISTER_CONFIG, self.mode)
        return res if res < 32768 else res - 65536

    def alert_start(self, rate=4, channel1=0, channel2=None,
                    threshold_high=0x4000, threshold_low=0, latched=False) :
        """Start continuous measurement, set ALERT pin on threshold."""
        self._write_register(_REGISTER_LOWTHRESH, threshold_low)
        self._write_register(_REGISTER_HITHRESH, threshold_high)
        self._write_register(_REGISTER_CONFIG, _CQUE_1CONV |
                             _CLAT_LATCH if latched else _CLAT_NONLAT |
                             _CPOL_ACTVLOW | _CMODE_TRAD | _RATES[rate] |
                             _MODE_CONTIN | _GAINS[self.gain] |
                             _CHANNELS[(channel1, channel2)])

    def conversion_start(self, rate=4, channel1=0, channel2=None):
        """Start continuous measurement, trigger on ALERT/RDY pin."""
        self._write_register(_REGISTER_LOWTHRESH, 0)
        self._write_register(_REGISTER_HITHRESH, 0x8000)
        self._write_register(_REGISTER_CONFIG, _CQUE_1CONV | _CLAT_NONLAT |
                             _CPOL_ACTVLOW | _CMODE_TRAD | _RATES[rate] |
                             _MODE_CONTIN | _GAINS[self.gain] |
                             _CHANNELS[(channel1, channel2)])

    def alert_read(self):
        """Get the last reading from the continuous measurement."""
        res = self._read_register(_REGISTER_CONVERT)
        return res if res < 32768 else res - 65536

    def read(self,pin):
        raw = self.read_raw(channel1=pin)
        voltage = self.raw_to_v(raw)
        return {"raw":raw,"voltage":voltage}




DATETIME_REG = const(0) # 0x00-0x06
CHIP_HALT    = const(128)
CONTROL_REG  = const(7) # 0x07
RAM_REG      = const(8) # 0x08-0x3F

# BME280 default address.
BME280_I2CADDR = 0x76

# Operating Modes
BME280_OSAMPLE_1 = 1
BME280_OSAMPLE_2 = 2
BME280_OSAMPLE_4 = 3
BME280_OSAMPLE_8 = 4
BME280_OSAMPLE_16 = 5

BME280_REGISTER_CONTROL_HUM = 0xF2
BME280_REGISTER_STATUS = 0xF3
BME280_REGISTER_CONTROL = 0xF4

MODE_SLEEP = const(0)
MODE_FORCED = const(1)
MODE_NORMAL = const(3)

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

class LightSensor():

    def __init__(self):

        # Define some constants from the datasheet

        self.DEVICE = 0x5c # Default device I2C address

        self.POWER_DOWN = 0x00 # No active state
        self.POWER_ON = 0x01 # Power on
        self.RESET = 0x07 # Reset data register value

        # Start measurement at 4lx resolution. Time typically 16ms.
        self.CONTINUOUS_LOW_RES_MODE = 0x13
        # Start measurement at 1lx resolution. Time typically 120ms
        self.CONTINUOUS_HIGH_RES_MODE_1 = 0x10
        # Start measurement at 0.5lx resolution. Time typically 120ms
        self.CONTINUOUS_HIGH_RES_MODE_2 = 0x11
        # Start measurement at 1lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        self.ONE_TIME_HIGH_RES_MODE_1 = 0x20
        # Start measurement at 0.5lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        self.ONE_TIME_HIGH_RES_MODE_2 = 0x21
        # Start measurement at 1lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        self.ONE_TIME_LOW_RES_MODE = 0x23
        # setup I2C
        self.i2c = machine.I2C(scl=machine.Pin(15), sda=machine.Pin(4))

    def convertToNumber(self, data):

        # Simple function to convert 2 bytes of data
        # into a decimal number
        return ((data[1] + (256 * data[0])) / 1.2)

    def readLight(self):

        data = self.i2c.readfrom_mem(self.DEVICE,self.ONE_TIME_HIGH_RES_MODE_1,2)
        return self.convertToNumber(data)

class BME280:

    def __init__(self,mode=BME280_OSAMPLE_8,address=BME280_I2CADDR,i2c=None,**kwargs):
        # Check that mode is valid.
        if mode not in [BME280_OSAMPLE_1, BME280_OSAMPLE_2, BME280_OSAMPLE_4,
                        BME280_OSAMPLE_8, BME280_OSAMPLE_16]:
            raise ValueError(
                'Unexpected mode value {0}. Set mode to one of '
                'BME280_OSAMPLE_1, BME280_OSAMPLE_2, BME280_OSAMPLE_4,'
                'BME280_OSAMPLE_8, BME280_OSAMPLE_16'.format(mode))
        self._mode = mode
        self.address = address
        if i2c is None:
            raise ValueError('An I2C object is required.')
        self.i2c = i2c
        self.__sealevel = 101325

        # load calibration data
        dig_88_a1 = self.i2c.readfrom_mem(self.address, 0x88, 26)
        dig_e1_e7 = self.i2c.readfrom_mem(self.address, 0xE1, 7)

        self.dig_T1, self.dig_T2, self.dig_T3, self.dig_P1, \
            self.dig_P2, self.dig_P3, self.dig_P4, self.dig_P5, \
            self.dig_P6, self.dig_P7, self.dig_P8, self.dig_P9, \
            _, self.dig_H1 = unpack("<HhhHhhhhhhhhBB", dig_88_a1)

        self.dig_H2, self.dig_H3, self.dig_H4,\
            self.dig_H5, self.dig_H6 = unpack("<hBbhb", dig_e1_e7)
        # unfold H4, H5, keeping care of a potential sign
        self.dig_H4 = (self.dig_H4 * 16) + (self.dig_H5 & 0xF)
        self.dig_H5 //= 16

        # temporary data holders which stay allocated
        self._l1_barray = bytearray(1)
        self._l8_barray = bytearray(8)
        self._l3_resultarray = array("i", [0, 0, 0])

        self._l1_barray[0] = self._mode << 5 | self._mode << 2 | MODE_SLEEP
        self.i2c.writeto_mem(self.address, BME280_REGISTER_CONTROL,
                             self._l1_barray)
        self.t_fine = 0

    def read_raw_data(self, result):
        """ Reads the raw (uncompensated) data from the sensor.
            Args:
                result: array of length 3 or alike where the result will be
                stored, in temperature, pressure, humidity order
            Returns:
                None
        """

        self._l1_barray[0] = self._mode
        self.i2c.writeto_mem(self.address, BME280_REGISTER_CONTROL_HUM,
                             self._l1_barray)
        self._l1_barray[0] = self._mode << 5 | self._mode << 2 | MODE_FORCED
        self.i2c.writeto_mem(self.address, BME280_REGISTER_CONTROL,
                             self._l1_barray)

        # Wait for conversion to complete
        while self.i2c.readfrom_mem(self.address, BME280_REGISTER_STATUS, 1)[0] & 0x08:
            time.sleep_ms(5)

        # burst readout from 0xF7 to 0xFE, recommended by datasheet
        self.i2c.readfrom_mem_into(self.address, 0xF7, self._l8_barray)
        readout = self._l8_barray
        # pressure(0xF7): ((msb << 16) | (lsb << 8) | xlsb) >> 4
        raw_press = ((readout[0] << 16) | (readout[1] << 8) | readout[2]) >> 4
        # temperature(0xFA): ((msb << 16) | (lsb << 8) | xlsb) >> 4
        raw_temp = ((readout[3] << 16) | (readout[4] << 8) | readout[5]) >> 4
        # humidity(0xFD): (msb << 8) | lsb
        raw_hum = (readout[6] << 8) | readout[7]

        result[0] = raw_temp
        result[1] = raw_press
        result[2] = raw_hum

    def read_compensated_data(self, result=None):
        """ Reads the data from the sensor and returns the compensated data.
            Args:
                result: array of length 3 or alike where the result will be
                stored, in temperature, pressure, humidity order. You may use
                this to read out the sensor without allocating heap memory
            Returns:
                array with temperature, pressure, humidity. Will be the one
                from the result parameter if not None
        """
        self.read_raw_data(self._l3_resultarray)
        raw_temp, raw_press, raw_hum = self._l3_resultarray
        # temperature
        var1 = (raw_temp/16384.0 - self.dig_T1/1024.0) * self.dig_T2
        var2 = raw_temp/131072.0 - self.dig_T1/8192.0
        var2 = var2 * var2 * self.dig_T3
        self.t_fine = int(var1 + var2)
        temp = (var1 + var2) / 5120.0
        temp = max(-40, min(85, temp))

        # pressure
        var1 = (self.t_fine/2.0) - 64000.0
        var2 = var1 * var1 * self.dig_P6 / 32768.0 + var1 * self.dig_P5 * 2.0
        var2 = (var2 / 4.0) + (self.dig_P4 * 65536.0)
        var1 = (self.dig_P3 * var1 * var1 / 524288.0 + self.dig_P2 * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * self.dig_P1
        if (var1 == 0.0):
            pressure = 30000  # avoid exception caused by division by zero
        else:
            p = ((1048576.0 - raw_press) - (var2 / 4096.0)) * 6250.0 / var1
            var1 = self.dig_P9 * p * p / 2147483648.0
            var2 = p * self.dig_P8 / 32768.0
            pressure = p + (var1 + var2 + self.dig_P7) / 16.0
            pressure = max(30000, min(110000, pressure))

        # humidity
        h = (self.t_fine - 76800.0)
        h = ((raw_hum - (self.dig_H4 * 64.0 + self.dig_H5 / 16384.0 * h)) *
             (self.dig_H2 / 65536.0 * (1.0 + self.dig_H6 / 67108864.0 * h *
                                       (1.0 + self.dig_H3 / 67108864.0 * h))))
        humidity = h * (1.0 - self.dig_H1 * h / 524288.0)

        if result:
            result[0] = temp
            result[1] = pressure
            result[2] = humidity
            return result

        return array("f", (temp, pressure, humidity))

    @property
    def sealevel(self):
        return self.__sealevel

    @sealevel.setter
    def sealevel(self, value):
        if 30000 < value < 120000:  # just ensure some reasonable value
            self.__sealevel = value

    @property
    def altitude(self):
        '''
        Altitude in m.
        '''
        from math import pow
        try:
            p = 44330 * (1.0 - pow(self.read_compensated_data()[1] /
                                   self.__sealevel, 0.1903))
        except:
            p = 0.0
        return p

    @property
    def dew_point(self):
        """
        Compute the dew point temperature for the current Temperature
        and Humidity measured pair
        """
        from math import log
        t, p, h = self.read_compensated_data()
        h = (log(h, 10) - 2) / 0.4343 + (17.62 * t) / (243.12 + t)
        return 243.12 * h / (17.62 - h)

    @property
    def values(self):
        """ human readable values """

        t, p, h = self.read_compensated_data()

        return ("{:.2f}C".format(t), "{:.2f}hPa".format(p/100),
                "{:.2f}%".format(h))

class DS1307(object):
    """Driver for the DS1307 RTC."""
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        self.weekday_start = 1
        self._halt = False

    def _dec2bcd(self, value):
        """Convert decimal to binary coded decimal (BCD) format"""
        return (value // 10) << 4 | (value % 10)

    def _bcd2dec(self, value):
        """Convert binary coded decimal (BCD) format to decimal"""
        return ((value >> 4) * 10) + (value & 0x0F)

    def datetime(self, datetime=None):
        """Get or set datetime"""
        if datetime is None:
            buf = self.i2c.readfrom_mem(self.addr, DATETIME_REG, 7)
            return (
                self._bcd2dec(buf[6]) + 2000, # year
                self._bcd2dec(buf[5]), # month
                self._bcd2dec(buf[4]), # day
                self._bcd2dec(buf[3] - self.weekday_start), # weekday
                self._bcd2dec(buf[2]), # hour
                self._bcd2dec(buf[1]), # minute
                self._bcd2dec(buf[0] & 0x7F), # second
                0 # subseconds
            )
        buf = bytearray(7)
        buf[0] = self._dec2bcd(datetime[6]) & 0x7F # second
        buf[1] = self._dec2bcd(datetime[5]) # minute
        buf[2] = self._dec2bcd(datetime[4]) # hour
        buf[3] = self._dec2bcd(datetime[3] + self.weekday_start) # weekday
        buf[4] = self._dec2bcd(datetime[2]) # day
        buf[5] = self._dec2bcd(datetime[1]) # month
        buf[6] = self._dec2bcd(datetime[0] - 2000) # year
        if (self._halt):
            buf[0] |= (1 << 7)
        self.i2c.writeto_mem(self.addr, DATETIME_REG, buf)

    def halt(self, val=None):
        """Power up, power down or check status"""
        if val is None:
            return self._halt
        reg = self.i2c.readfrom_mem(self.addr, DATETIME_REG, 1)[0]
        if val:
            reg |= CHIP_HALT
        else:
            reg &= ~CHIP_HALT
        self._halt = bool(val)
        self.i2c.writeto_mem(self.addr, DATETIME_REG, bytearray([reg]))

    def square_wave(self, sqw=0, out=0):
        """Output square wave on pin SQ at 1Hz, 4.096kHz, 8.192kHz or 32.768kHz,
        or disable the oscillator and output logic level high/low."""
        rs0 = 1 if sqw == 4 or sqw == 32 else 0
        rs1 = 1 if sqw == 8 or sqw == 32 else 0
        out = 1 if out > 0 else 0
        sqw = 1 if sqw > 0 else 0
        reg = rs0 | rs1 << 1 | sqw << 4 | out << 7
        self.i2c.writeto_mem(self.addr, CONTROL_REG, bytearray([reg]))

# register addresses in port=0, bank=1 mode (easier maths to convert)
_MCP_IODIR        = const(0x00) # R/W I/O Direction Register
_MCP_IPOL         = const(0x01) # R/W Input Polarity Port Register
_MCP_GPINTEN      = const(0x02) # R/W Interrupt-on-Change Pins
_MCP_DEFVAL       = const(0x03) # R/W Default Value Register
_MCP_INTCON       = const(0x04) # R/W Interrupt-on-Change Control Register
_MCP_IOCON        = const(0x05) # R/W Configuration Register
_MCP_GPPU         = const(0x06) # R/W Pull-Up Resistor Register
_MCP_INTF         = const(0x07) # R   Interrupt Flag Register (read clears)
_MCP_INTCAP       = const(0x08) # R   Interrupt Captured Value For Port Register
_MCP_GPIO         = const(0x09) # R/W General Purpose I/O Port Register
_MCP_OLAT         = const(0x0a) # R/W Output Latch Register

# Config register (IOCON) bits
_MCP_IOCON_INTPOL = const(2)
_MCP_IOCON_ODR    = const(4)
_MCP_IOCON_DISSLW = const(16)
_MCP_IOCON_SEQOP  = const(32)
_MCP_IOCON_MIRROR = const(64)
_MCP_IOCON_BANK   = const(128)


class Port():
    # represents one of the two 8-bit ports
    def __init__(self, port, mcp):
        self._port = port & 1
        self._mcp = mcp

    def _which_reg(self, reg):
        if self._mcp._config & 0x80 == 0x80:
            return reg | (self._port << 4)
        else:
            return (reg << 1) + self._port

    def _flip_property_bit(self, reg, condition, bit):
        if condition:
            setattr(self, reg, getattr(self, reg) | bit)
        else:
            setattr(self, reg, getattr(self, reg) & ~bit)

    def _read(self, reg):
        return self._mcp._i2c.readfrom_mem(self._mcp._address, self._which_reg(reg), 1)[0]

    def _write(self, reg, val):
        val &= 0xff
        self._mcp._i2c.writeto_mem(self._mcp._address, self._which_reg(reg), bytearray([val]))
        # if writing to the config register, make a copy in mcp so that it knows
        # which bank you're using for subsequent writes
        if reg == _MCP_IOCON:
            self._mcp._config = val

    @property
    def mode(self):
        return self._read(_MCP_IODIR)
    @mode.setter
    def mode(self, val):
        self._write(_MCP_IODIR, val)

    @property
    def input_polarity(self):
        return self._read(_MCP_IPOL)
    @input_polarity.setter
    def input_polarity(self, val):
        self._write(_MCP_IPOL, val)

    @property
    def interrupt_enable(self):
        return self._read(_MCP_GPINTEN)
    @interrupt_enable.setter
    def interrupt_enable(self, val):
        self._write(_MCP_GPINTEN, val)

    @property
    def default_value(self):
        return self._read(_MCP_DEFVAL)
    @default_value.setter
    def default_value(self, val):
        self._write(_MCP_DEFVAL, val)

    @property
    def interrupt_compare_default(self):
        return self._read(_MCP_INTCON)
    @interrupt_compare_default.setter
    def interrupt_compare_default(self, val):
        self._write(_MCP_INTCON, val)

    @property
    def io_config(self):
        return self._read(_MCP_IOCON)
    @io_config.setter
    def io_config(self, val):
        self._write(_MCP_IOCON, val)

    @property
    def pullup(self):
        return self._read(_MCP_GPPU)
    @pullup.setter
    def pullup(self, val):
        self._write(_MCP_GPPU, val)

    # read only
    @property
    def interrupt_flag(self):
        return self._read(_MCP_INTF)

    # read only
    @property
    def interrupt_captured(self):
        return self._read(_MCP_INTCAP)

    @property
    def gpio(self):
        return self._read(_MCP_GPIO)
    @gpio.setter
    def gpio(self, val):
        # writing to this register modifies the OLAT register for pins configured as output
        self._write(_MCP_GPIO, val)

    @property
    def output_latch(self):
        return self._read(_MCP_OLAT)
    @output_latch.setter
    def output_latch(self, val):
        # modifies the output latches on pins configured as outputs
        self._write(_MCP_OLAT, val)


class MCP23017():
    def __init__(self, i2c, address=0x20):
        self._i2c = i2c
        self._address = address
        self._config = 0x00
        self._virtual_pins = {}
        self.init()

    def init(self):
        # error if device not found at i2c addr
        if self._i2c.scan().count(self._address) == 0:
            raise OSError('MCP23017 not found at I2C address {:#x}'.format(self._address))

        self.porta = Port(0, self)
        self.portb = Port(1, self)

        self.io_config = 0x00      # io expander configuration - same on both ports, only need to write once

        # Reset to all inputs with no pull-ups and no inverted polarity.
        self.mode = 0xFFFF                       # in/out direction (0=out, 1=in)
        self.input_polarity = 0x0000             # invert port input polarity (0=normal, 1=invert)
        self.interrupt_enable = 0x0000           # int on change pins (0=disabled, 1=enabled)
        self.default_value = 0x0000              # default value for int on change
        self.interrupt_compare_default = 0x0000  # int on change control (0=compare to prev val, 1=compare to def val)
        self.pullup = 0x0000                     # gpio weak pull up resistor - when configured as input (0=disabled, 1=enabled)
        self.gpio = 0x0000                       # port (0=logic low, 1=logic high)

    def config(self, interrupt_polarity=None, interrupt_open_drain=None, sda_slew=None, sequential_operation=None, interrupt_mirror=None, bank=None):
        io_config = self.porta.io_config

        if interrupt_polarity is not None:
            # configre INT as push-pull
            # 0: Active low
            # 1: Active high
            io_config = self._flip_bit(io_config, interrupt_polarity, _MCP_IOCON_INTPOL)
            if interrupt_polarity:
                # if setting to 1, unset ODR bit - interrupt_open_drain
                interrupt_open_drain = False
        if interrupt_open_drain is not None:
            # configure INT as open drain, overriding interrupt_polarity
            # 0: INTPOL sets the polarity
            # 1: Open drain, INTPOL ignored
            io_config = self._flip_bit(io_config, interrupt_open_drain, _MCP_IOCON_ODR)
        if sda_slew is not None:
            # 0: Slew rate function on SDA pin enabled
            # 1: Slew rate function on SDA pin disabled
            io_config = self._flip_bit(io_config, sda_slew, _MCP_IOCON_DISSLW)
        if sequential_operation is not None:
            # 0: Enabled, address pointer increments
            # 1: Disabled, address pointer fixed
            io_config = self._flip_bit(io_config, sequential_operation, _MCP_IOCON_SEQOP)
        if interrupt_mirror is not None:
            # 0: Independent INTA,INTB pins
            # 1: Internally linked INTA,INTB pins
            io_config = self._flip_bit(io_config, interrupt_mirror, _MCP_IOCON_MIRROR)
        if bank is not None:
            # 0: Registers alternate between A and B ports
            # 1: All port A registers first then all port B
            io_config = self._flip_bit(io_config, bank, _MCP_IOCON_BANK)

        # both ports share the same register, so you only need to write on one
        self.porta.io_config = io_config
        self._config = io_config

    def _flip_bit(self, value, condition, bit):
        if condition:
            value |= bit
        else:
            value &= ~bit
        return value

    def pin(self, pin, mode=None, value=None, pullup=None, polarity=None, interrupt_enable=None, interrupt_compare_default=None, default_value=None):
        assert 0 <= pin <= 15
        port = self.portb if pin // 8 else self.porta
        bit = (1 << (pin % 8))
        if mode is not None:
            # 0: Pin is configured as an output
            # 1: Pin is configured as an input
            port._flip_property_bit('mode', mode & 1, bit)
        if value is not None:
            # 0: Pin is set to logic low
            # 1: Pin is set to logic high
            port._flip_property_bit('gpio', value & 1, bit)
        if pullup is not None:
            # 0: Weak pull-up 100k ohm resistor disabled
            # 1: Weak pull-up 100k ohm resistor enabled
            port._flip_property_bit('pullup', pullup & 1, bit)
        if polarity is not None:
            # 0: GPIO register bit reflects the same logic state of the input pin
            # 1: GPIO register bit reflects the opposite logic state of the input pin
            port._flip_property_bit('input_polarity', polarity & 1, bit)
        if interrupt_enable is not None:
            # 0: Disables GPIO input pin for interrupt-on-change event
            # 1: Enables GPIO input pin for interrupt-on-change event
            port._flip_property_bit('interrupt_enable', interrupt_enable & 1, bit)
        if interrupt_compare_default is not None:
            # 0: Pin value is compared against the previous pin value
            # 1: Pin value is compared against the associated bit in the DEFVAL register
            port._flip_property_bit('interrupt_compare_default', interrupt_compare_default & 1, bit)
        if default_value is not None:
            # 0: Default value for comparison in interrupt, when configured to compare against DEFVAL register
            # 1: Default value for comparison in interrupt, when configured to compare against DEFVAL register
            port._flip_property_bit('default_value', default_value & 1, bit)
        if value is None:
            return port.gpio & bit == bit

    def interrupt_triggered_gpio(self, port):
        # which gpio triggered the interrupt
        # only 1 bit will be set
        port = self.portb if port else self.porta
        return port.interrupt_flag

    def interrupt_captured_gpio(self, port):
        # captured gpio values at time of int
        # reading this will clear the current interrupt
        port = self.portb if port else self.porta
        return port.interrupt_captured

    # mode (IODIR register)
    @property
    def mode(self):
        return self.porta.mode | (self.portb.mode << 8)
    @mode.setter
    def mode(self, val):
        self.porta.mode = val
        self.portb.mode = (val >> 8)

    # input_polarity (IPOL register)
    @property
    def input_polarity(self):
        return self.porta.input_polarity | (self.portb.input_polarity << 8)
    @input_polarity.setter
    def input_polarity(self, val):
        self.porta.input_polarity = val
        self.portb.input_polarity = (val >> 8)

    # interrupt_enable (GPINTEN register)
    @property
    def interrupt_enable(self):
        return self.porta.interrupt_enable | (self.portb.interrupt_enable << 8)
    @interrupt_enable.setter
    def interrupt_enable(self, val):
        self.porta.interrupt_enable = val
        self.portb.interrupt_enable = (val >> 8)

    # default_value (DEFVAL register)
    @property
    def default_value(self):
        return self.porta.default_value | (self.portb.default_value << 8)
    @default_value.setter
    def default_value(self, val):
        self.porta.default_value = val
        self.portb.default_value = (val >> 8)

    # interrupt_compare_default (INTCON register)
    @property
    def interrupt_compare_default(self):
        return self.porta.interrupt_compare_default | (self.portb.interrupt_compare_default << 8)
    @interrupt_compare_default.setter
    def interrupt_compare_default(self, val):
        self.porta.interrupt_compare_default = val
        self.portb.interrupt_compare_default = (val >> 8)

    # io_config (IOCON register)
    # This register is duplicated in each port. Changing one changes both.
    @property
    def io_config(self):
        return self.porta.io_config
    @io_config.setter
    def io_config(self, val):
        self.porta.io_config = val

    # pullup (GPPU register)
    @property
    def pullup(self):
        return self.porta.pullup | (self.portb.pullup << 8)
    @pullup.setter
    def pullup(self, val):
        self.porta.pullup = val
        self.portb.pullup = (val >> 8)

    # interrupt_flag (INTF register)
    # read only
    @property
    def interrupt_flag(self):
        return self.porta.interrupt_flag | (self.portb.interrupt_flag << 8)

    # interrupt_captured (INTCAP register)
    # read only
    @property
    def interrupt_captured(self):
        return self.porta.interrupt_captured | (self.portb.interrupt_captured << 8)

    # gpio (GPIO register)
    @property
    def gpio(self):
        return self.porta.gpio | (self.portb.gpio << 8)
    @gpio.setter
    def gpio(self, val):
        self.porta.gpio = val
        self.portb.gpio = (val >> 8)

    # output_latch (OLAT register)
    @property
    def output_latch(self):
        return self.porta.output_latch | (self.portb.output_latch << 8)
    @output_latch.setter
    def output_latch(self, val):
        self.porta.output_latch = val
        self.portb.output_latch = (val >> 8)

    # list interface
    # mcp[pin] lazy creates a VirtualPin(pin, port)
    def __getitem__(self, pin):
        assert 0 <= pin <= 15
        if not pin in self._virtual_pins:
            self._virtual_pins[pin] = VirtualPin(pin, self.portb if pin // 8 else self.porta)
        return self._virtual_pins[pin]

class VirtualPin():
    def __init__(self, pin, port):
        self._pin = pin % 8
        self._bit = 1 << self._pin
        self._port = port

    def _flip_bit(self, value, condition):
        return value | self._bit if condition else value & ~self._bit

    def _get_bit(self, value):
        return (value & self._bit) >> self._pin

    def value(self, val=None):
        # if val, write, else read
        if val is not None:
            self._port.gpio = self._flip_bit(self._port.gpio, val & 1)
        else:
            return self._get_bit(self._port.gpio)

    def input(self, pull=None):
        # if pull, enable pull up, else read
        self._port.mode = self._flip_bit(self._port.mode, 1)
        if pull is not None:
            self._port.pullup = self._flip_bit(self._port.pullup, pull & 1) # toggle pull up

    def output(self, val=None):
        # if val, write, else read
        self._port.mode = self._flip_bit(self._port.mode, 0)
        if val is not None:
            self._port.gpio = self._flip_bit(self._port.gpio, val & 1)
