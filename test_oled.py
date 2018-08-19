# demo readings from DHT22 temperature sensor
# test for class OLED in oled.py
#
# Configuration:
# DHT22 sensor attached to GPIO15
# OLED display ssd1306 on i2c (SDA/SCL)
#
# 2018_0529 PePo using class OLED in lib/old.py
#           Loboris micropython tested OKAY
# URL: https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/onewire
# #############################################
from micropython import const
import machine, time
import oled, dhtsensor
from utils import readjson
from ledsignal import LedSignal

# Configuration
# read I2C characteristics
i2c_config = readjson('i2c.json')
pinSda      = int(i2c_config["SDA"]) #const(22)  # ESP32 - GPIO22
pinScl      = int(i2c_config["SCL"]) #const(21)  # ESP32 - GPIO21

# DHT config
dht_config = readjson('dht.json')
pinDht      = int(dht_config["GPIO"]) #const(15) # data-pin DHTxx sensor

# read I2C-OLED characteristics
oled_config = readjson('oled.json')
hSize       = int(oled_config["HEIGHT"]) #const(64)#(32)  # display heigh in pixels
wSize       = int(oled_config["WIDTH"]) #const(128) # display width in pixels
addrOled    = int(oled_config["I2C_ADDRESS"]) #const(60)  #0x3c

# other devices
#addrBME280  = 118 #0x76
pinLed      = const(5) # builtin LED for ESP32-WROVER/WeMOS Lolin32

#cleanup
import gc
gc.collect()

# get current timerecord
def timerecord():
    return time.strftime("%a %d %b %Y %H:%M:%S", time.localtime())

# display sensor data (serial port and connected OLED)
def showSensorData(display, temp, hum):
    # print on console/serial connection
    print('{0}: Temperature {1} C, Humidity {2} %'.format(timerecord(), temp, hum))

    # show on connected OLED display
    if display.isconnected:
        display.clear(False) # clear real screen
        # x, y calculations...
        row = 0
        dy = const(12) # distance in rows
        # oky, some fancy calculation:
        # if heigt OLED >= 64, skip a line between data and header
        my = const(2) if hSize >= 64 else const(1)

        # HEADER line
        #msg = 'DHT22 '
        #only date: msg = time.strftime("DHT22 %Y-%m-%d %H:%M", time.localtime())
        # format: 29 May 20:54
        msg = time.strftime("%d %b %H:%M", time.localtime())
        display.message(msg, 0, row) # start HEADER in middle of screen
        #display.message(msg, 20, row) # start HEADER in middle of screen

        # Temperature line
        msg = "{0} {1} {2}".format('Temp.', temp, 'C')
        display.message(msg, 0, row + my * dy)

        # Humidity line, last line -> show onscreen
        msg = "{0} {1} {2}".format('Hum. ', hum, '%')
        display.message(msg, 0, row + (my+1) * dy, True)



# heart image for display on the OLED screen.
# 1-color screen: set each pixel to either on 1 or off 0.
HEART = [
[ 0, 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 1, 1, 0, 0, 0, 1, 1, 0],
[ 1, 1, 1, 1, 0, 1, 1, 1, 1],
[ 1, 1, 1, 1, 1, 1, 1, 1, 1],
[ 1, 1, 1, 1, 1, 1, 1, 1, 1],
[ 0, 1, 1, 1, 1, 1, 1, 1, 0],
[ 0, 0, 1, 1, 1, 1, 1, 0, 0],
[ 0, 0, 0, 1, 1, 1, 0, 0, 0],
[ 0, 0, 0, 0, 1, 0, 0, 0, 0],
]

# demo: read temperature each dt seconds
# forever, until interrupted by Ctrl-C
# default 2 seconds - DHT22
def demo(dt=2):
    try:
        # init i2c
        i2c = machine.I2C(scl=machine.Pin(pinScl), sda=machine.Pin(pinSda))

        # init OLED SSD1306_I2C object
        display = oled.OLED(wSize, hSize, i2c, addrOled)

        #create a temperature sensor
        dht = dhtsensor.DHTSensor(pinDht, machine.DHT.DHT2X)
        dhtIsConnected = True

        # create led
        led = LedSignal(pinLed, True)
        led.off()

        # center icon on display
        l = len(HEART)
        w, h = wSize, hSize
        #show_icon(display, HEART, dx, dy)   # centered icon
        #show_icon(display, HEART)           # left-top icon
        #show_icon(display, HEART, 0, (h-l)) # left-bottom icon
        #display.show_icon(HEART, (w-l))    # right-top icon
        #show_icon(display, HEART, (w-l), (h-l) ) # right-bottom icon

        while True:
            led.on()
            display.show_icon(HEART, (w-l))    # right-top icon

            temp, hum = dht.read()
            #print('Temperature {0} C, Humidity {1} %'.format(temp, hum))
            showSensorData(display, temp, hum)

            led.off()
            #display.show_icon(HEART, (w-l), (h-l) ) # right-bottom icon
            time.sleep(dt)

    except KeyboardInterrupt:
        display.clear(True) # clear display
        i2c.deinit() # de-init i2c
        print('done.')

#print("usage: ", __name__, ".demo()")
if __name__ == "__main__":
    demo()
else:
    print("Usage: {0}.{1}".format(__name__, "demo()"))
