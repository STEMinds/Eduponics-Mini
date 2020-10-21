# STEMinds Eduponics Mini MicroPython repository

In this repository you'll find all the example code necessary to get started with your Eduponics mini ESP32 learning kit.
The MQTT client found in the eduponics_mqtt folder can be used with the Eduponics Mini app which is currently available on the Android play store (search for "Eduponics") and soon will be available on the Apple appstore.

## Documentation

The entire documentation is freely available at STEMinds wiki: [wiki.steminds.com](https://wiki.steminds.com/kits/eduponics_mini/introduction/)
Feel free to follow along or just go to the bottom to understand how to connect and use the Eduponics mobile app combined with Eduponics mini kit.

## Configuring WiFi for the MQTT client

All the code should work AS IS the only modification required is for the *boot.py* python file to modify the WiFi SSID and Password in order for the ESP32 to connect successfully to your home WiFi. From there, the Eduponics Mini can be controlled from anywhere, even outside of your own network.
## License

Some of the code is taken from other repositories, proper credits and license is given at the beginning of each file.
All the example code and files are under MIT License.

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
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
