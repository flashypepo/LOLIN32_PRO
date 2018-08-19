# demo readings from DHT22 temperature sensor
#
# Configuration:
# DHT22 sensor attached to GPIO15
# OLED display ssd1306 on i2c (SDA/SCL)
#
# 2018_0529 PePo Loboris micropython tested OKAY
# URL: https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/onewire
# #############################################
from micropython import const
import machine, time
import ssd1306, dhtsensor


# Configuration
pinSda      = const(22)  # ESP32 - GPIO22
pinScl      = const(21)  # ESP32 - GPIO21
pinLed      = const(5) # builtin LED for ESP32-WROVER/WeMOS Lolin32
pinDht      = const(15) # data-pin DHTxx sensor
addrOled    = const(60)  #0x3c
#addrBME280  = 118 #0x76
hSize       = const(32)  # display heigh in pixels
wSize       = const(128) # display width in pixels

oledIsConnected = False
dhtIsConnected  = False
#bmeIsConnected  = False

# sensor values
temp = 0 #temperature value
hum = 0 # humidity value

# init and scan I2C for devices
i2c = machine.I2C(scl=machine.Pin(pinScl), sda=machine.Pin(pinSda))

# scan I2C bus for devices
print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
  #print("No i2c device !")
  raise Exception("No i2c device!")

print('i2c devices found:',len(devices))
for device in devices:
    if device == addrOled:
        oledIsConnected = True
    #if device == addrBME280:
    #    bmeIsConnected = True
    print(device)

# OLED SSD1306_I2C object
if oledIsConnected:
  oled = ssd1306.SSD1306_I2C(wSize, hSize, i2c, addrOled)
  oled.fill(0) # erase screen content

#create a temperature sensor
dht = dhtsensor.DHTSensor(pinDht, machine.DHT.DHT2X)
dhtIsConnected = True

# create led
from ledsignal import LedSignal
led = LedSignal(pinLed, True)
led.off()

def showSensorData(temp, hum):
    print('Temperature {0} C, Humidity {1} %'.format(temp, hum))
    if oledIsConnected:
        oled.fill(0) # clear screen
        y = 0
        oled.text('DHT22:', 0, y)
        oled.text('T:{0} C'.format(temp), 0, y+10)
        oled.text('H:{0} %'.format(hum), 0, y+20)
        oled.show()

# demo: read temperature each dt seconds forever
def demo(dt=2):
    try:
        while True:
            led.on()
            temp, hum = dht.read()
            #print('Temperature {0} C, Humidity {1} %'.format(temp, hum))
            showSensorData(temp, hum)
            led.off()
            time.sleep(dt)

    except KeyboardInterrupt:
        oled.fill(0) #clear oled
        oled.show()
        i2c.deinit() # de-initialise i2c
        print('done.')

#print("usage: ", __name__, ".demo()")
#demo()
print("Usage: {0}.{1}".format(__name__, "demo()"))
