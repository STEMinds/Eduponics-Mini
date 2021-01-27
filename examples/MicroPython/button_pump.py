import machine
import esp32
import time

# define pump on pin IO23 as OUTPUT
pump = machine.Pin(23, machine.Pin.OUT, machine.Pin.PULL_UP)
# define water level sensor as INPUT on IO pin number 21
water_level = machine.Pin(21, machine.Pin.IN)
# define wakeup button and callback
wake_up = machine.Pin(36, mode = machine.Pin.IN)

def water_level_change(pin):
    return 1

def wakeup_pressed(pin):
    # turn on the pump
    pump.value(pin)
    print("pressed")

# define the callbacks for the sensors
water_level.irq(trigger=machine.Pin.IRQ_FALLING, handler=water_level_change)
wake_up.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=wakeup_pressed)
