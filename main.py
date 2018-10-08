"""
main.py
2018-0923 PePo - add DHT22 and MQTT, server=MQTT_SERVER
2018-0819 PePo - changed to Adafruit OLED-SPI display (test)
2018-0529 PePo - startup Wifi connection
* WifiManager and wificonfig.json
* added rtc sync with NTP-server
* added temperature experiment on OLED
"""

USE_DEBUG = True

# #################################
# cleanup
# #################################
import gc
gc.collect()
if USE_DEBUG:
    print('main - start: mem_free = {} bytes'.format(gc.mem_free()))


# specify attached devices...
use_WIFI = True

use_OLED_I2C = False
use_OLED_SPI = False
use_DHT22 = True

use_MQTT = False

# DEBUG-aid: LED GPIO5 is blinking (interrupt-based)
use_heartbeat = False

# #################################
# connect to Wifi network
# specifications in wificonfig.json
# #################################
if use_WIFI:
    import wifimanager

    print('main.py: connecting to network (wificonfig.json)...')
    wifi = wifimanager.WifiManager("wificonfig.json")
    params = wifi.connect()
    if USE_DEBUG:
        print('Device  IP = {0}'.format(params[0]))
        print('Gateway IP = {0}'.format(params[2]))
        #print('netwerk config = {}'.format(params))
        #wifi.print_config()

# #################################
# RTC sync
# #################################
    import rtc_sync


# #################################
# Experiment:
# Temperature measurement (DHT22)
# requires: OLED & DHT22 attached
# 2018-0324 Peter
# #################################
if use_OLED_I2C and use_DHT22:
    from test_oled import demo
    demo(5) # run experiment

# #################################
# Experiment:
# Adafruit 128*32, OLED-SPI display
# requires: SPI
# 2018-0819 Peter
# #################################
if use_OLED_SPI:
    from test_oled_spi import demo
    demo()

# #################################
# Experiment: temperature and humidity
# requires: DHT22 on Pin GPIOxx
# 2018-0923 Peter
# #################################
if use_DHT22:
    import machine, dhtsensor, time
    dht = dhtsensor.DHTsensor(15, machine.DHT.DHT2X)
    #def run(self, dt=10):
    print('DHT type:', dht.type)
    print('Sensor:', dht.sensor)
    print('Sensor-pin:', dht.pin)

    while True:
        t, h = self.read()
        print('t={0} C, h={1} % RH'.format(t, int(h)))
        sleep(5)

# #################################
# Experiment: MQTT and DHT22
# requires: DHT22 on Pin GPIOxx
# 2018-0923 Peter
# #################################
if use_MQTT and use_DHT22:
    MQTT_SERVER = '192.168.178.29'
    print('TODO: MQTT publish... to server:', MQTT_SERVER)

# #################################
# cleanup
# #################################
gc.collect()
if USE_DEBUG:
    print('main - end: mem_free = {} bytes'.format(gc.mem_free()))
