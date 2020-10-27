# How to use the IDF3 firmware

The IDF3 ESP32 firmware is generic firmware. it will work both on Arduino IDE and MicroPython.
We install and test the MicroPython version when we ship the products, if you want to use the Arduino IDE you can but note:

Once you use the Arduino IDE you might not be able to use Thonny IDE (MicroPython) again so easily, Thonny IDE might tell you:

      Could not enter REPL. Trying again with 1 second waiting time...

This result in Arduino IDE removing REPL (The MicroPython interpreter) in order to solve it, go to your Thonny IDE settings and press "Open the dialog for installing or upgrading MicroPython" and select the firmware esp32-idf3-20200902-v1.13.bin

This will install REPL again and you'll be able to use MicroPython without any problem.
