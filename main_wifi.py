"""
main.py
2018-0529 PePo - startup Wifi connection
* WifiManager and wificonfig.json
* added rtc sync with NTP-server
* added temperature experiment on OLED
"""

USE_DEBUG = False #True

# #################################
# connect to Wifi network
# specifications in wificonfig.json
# #################################
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
# cleanup
# #################################
import gc
gc.collect()
if USE_DEBUG:
    print('main: mem_free = {} bytes'.format(gc.mem_free()))

# #################################
# Experiment:
# Temperature measurement (DHT22)
# requires: OLED & DHT22 attached
# #################################
from test_oled import demo
demo() # run experiment
