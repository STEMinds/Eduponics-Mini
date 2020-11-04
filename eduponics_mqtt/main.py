"""
MicroPython MQTT Eduponics APP Client
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

from umqttsimple import MQTTClient
from dependencies import *
import machine
import time
import json

# set adc (analog to digital) on pin 35
adc = machine.ADC(machine.Pin(35))
# set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
adc.atten(machine.ADC.ATTN_11DB)

# Configure light sensor
light_sensor = LightSensor()

# Configure BME280
# setup I2C connection
i2c = machine.I2C(scl=machine.Pin(15), sda=machine.Pin(4))
# Initialize BME280 object with default address 0x76
bme_sensor = BME280(i2c=i2c)
# initialize dht object, DHT11 coonected to IO19
#d = dht.DHT11(machine.Pin(19))

# define water level sensor as INPUT on IO pin number 21
water_level = machine.Pin(21, machine.Pin.IN)

# define pump on pin IO23 as OUTPUT
pump = machine.Pin(23, machine.Pin.OUT)

# MQTT Unique ID
UUID = "YOUR_UUID_GENERATED_ID"
# MQTT Topics
topics = ["plants/soil","plants/environment","plants/water"]

def get_soil_moisture():

    # sensor min and max values
    # can be changed and callibrated
    minVal = 710
    maxVal = 4095

    # read soil moisture sensor data
    val = adc.read()

    # scale the value based on maxVal and minVal
    scale = 100 / (minVal - maxVal)
    # get calculated scale
    normal_reading = ("%s%s" % (int((val - maxVal) * scale),"%"))
    # we can also get inverted value if needed
    inverted_reading = ("%s%s" % (int((minVal - val) * scale),"%"))
    # for this example we'll return only the normal reading
    # put everything in a JSON format suitable for the eduponics app
    plant = {
        "id":0,
        "name":"Plant A",
        "enabled":1,
        "moisture":normal_reading
    }
    # return the data
    return str(plant).replace("'",'"')

def get_environmental_data():

    # get light from the light sensor
    lux = int(light_sensor.readLight())
    # get bme280 sensor data
    bme280_values = bme_sensor.values
    temperature = bme280_values[0].replace("C","")
    pressure = bme280_values[1]
    humidity = bme280_values[2].replace("%","")
    # get DHT11 sensor data
    # measure sensor data
    #d.measure()
    # get temperature and humidity
    #temperature = d.temperature()
    #humidity = d.humidity()
    # get water quantity
    water_quantity = water_level.value()

    # put all this data into a JSON object
    data = {
        "temp":temperature,
        "humidity":humidity,
        "sunlight":lux,
        "water_quantity":water_quantity
    }

    return str(data).replace("'",'"')

def water_plant():

    # turn on the pump
    pump.value(1)
    # get water quantity
    water_quantity = water_level.value()
    # if water level is not empty, keep doing it
    while not water_quantity == 1:
        # not empty and plant water is not full yet, keep giving water
        # check if soil moisture is bigger than 60
        if(int(json.loads(get_soil_moisture())["moisture"].replace("%","")) > 60):
            # enough water, stop giving water
            break;
        # wait for half a second and check again
        time.sleep(0.5)
        # get water quantity updated value
        water_quantity = water_level.value()

    # turn the pump off, either plant has enough water or no water at all.
    pump.value(0)
    return True

def on_message_callback(topic, msg):
    '''
    this is a callback, will be called when the app asks for certain information
    such as to water the plants when the watering button pressed
    '''
    # convert topic and message byte to string
    topic = str(topic, 'utf-8')
    msg = json.loads(str(msg, 'utf-8'))

    if(topic == "%s/plants/soil" % UUID or topic == "%s/plants/environment" % UUID):
        # Do nothing, we only publish to those topics
        pass
    elif(topic == "%s/plants/water" % UUID):
        # when the app request for plant watering it goes here
        if("key" in msg and "status" in msg):
            # valid request, let's process it
            if(msg["status"] == "pending"):
                # it's waiting for us to water it, let's water it
                water_plant()
                # after watering, publish success message of watering
                response = {"key":msg["key"],"status":"ok"}
                client.publish("%s/plants/water" % UUID, str(response).replace("'",'"'))
    else:
        print((topic, msg))

def connect_and_subscribe():

    print("[-] Connecting to MQTT client ...")
    # set the MQTT broker object
    client = MQTTClient()
    # set a callback for incoming messages (subscribed topics)
    client.set_callback(on_message_callback)
    # connect to the broker
    client.connect()

    # subscribe to the topics
    for topic in topics:
        client.subscribe("%s/%s" % (UUID,topic))
        print("[-] Subscribed to %s successfully" % topic)
        print("[-] Connected to %s MQTT broker successfully" % client.server)

    return client

def restart_and_reconnect():
    # something  went wrong, reconnect in 5 seconds ...
    print('[-] Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

# configure few variables
last_message = 0
message_interval = 1
previous_soil_moisture = "0%"

while True:
    try:
        # check if there are new messages pending to be processed
        # if there are, redirect them to callback on_message_callback()
        client.check_msg()

        # check if the last published data wasn't less than message_interval
        if (time.time() - last_message) > message_interval:
            # get soil moisture
            current_soil_moisture = get_soil_moisture()
            # check if previous data and new data is the same
            if(previous_soil_moisture != current_soil_moisture):
                # it's not the same, publish the new data
                previous_soil_moisture = current_soil_moisture
                client.publish("%s/plants/soil" % UUID, current_soil_moisture)
                #print("[-] published soil moisture")

            # update environmetal data
            env = get_environmental_data()
            client.publish("%s/plants/environment" % UUID, env)
            #print("[-] published evironmental data")

            # update last message timestamp
            last_message = time.time()

    except OSError as e:
        # if something goes wrong, reconnct to MQTT server
        restart_and_reconnect()
