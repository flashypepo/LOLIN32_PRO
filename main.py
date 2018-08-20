"""
main.py
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
WIFI_PRESENT = True
OLED_I2C_PRESENT = False
DHT22_PRESENT = False
OLED_SPI_PRESENT = True


# #################################
# connect to Wifi network
# specifications in wificonfig.json
# #################################
if WIFI_PRESENT:
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
if OLED_I2C_PRESENT and DHT22_PRESENT:
    from test_oled import demo
    demo(5) # run experiment

# #################################
# Experiment:
# Adafruit 128*32, OLED-SPI display
# requires: SPI
# 2018-0819 Peter
# #################################
if OLED_SPI_PRESENT:
    from test_oled_spi import demo
    demo()

# #################################
# cleanup
# #################################
gc.collect()
if USE_DEBUG:
    print('main - end: mem_free = {} bytes'.format(gc.mem_free()))
