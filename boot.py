"""
boot.py: this file is executed on every boot (including wake-boot from deepsleep)

2018-1008 pepo - tried to startup Wifi connection
    * WifiManager and wificonfig.json
    * added rtc sync with NTP-server
    ERROR: includes are not found, sys.path ???
"""
import sys
sys.path[1] = '/flash/lib'

import gc

#''' create Wifi object
import wifimanager
wifi = wifimanager.WifiManager("config/wificonfig_lolin32pro.json")
# connect to Wifi network
wifi.connect()
print('[boot.py] Device IP: {0}'.format(wifi._wlan.ifconfig()[0])) #device IP
# RTC sync
import rtc_sync

# Change password for telnet, ftp..
#2018-1007 TODO: wifi.change_access('pepo', 'plasma')

# print MAC-address
print('[boot.py] MAC:', wifi.mac)
#'''

# cleanup
gc.collect()
print('[boot.py] mem_free = {} bytes'.format(gc.mem_free()))
