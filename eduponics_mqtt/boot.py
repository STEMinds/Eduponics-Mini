from umqttsimple import MQTTClient
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

ssid = 'WIFI_NAME'
password = 'WIFI_PASSWORD'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connected to WiFi successfully, IP: %s' % station.ifconfig()[0])
