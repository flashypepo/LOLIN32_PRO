'''
 Test_OLED display Adafruit 128*32 SPI

 ESSENTIAL: display Vin >= 3.3V, use a battery

 Pin connections
 Display   LoLin32
 Vin       5V (or BAT + LiPo battery), Vin>3.3V
 GND       GND
 DATA      15 - MOSI
 CLK       14 - SCK/CLK
   -        2 - MISO (not used)
 CS        23       13 is reserved for SD
 DC        21       reserved 12, or 4 for SD
 RST       22           ,,
 3.3V0      not used
'''
from machine import Pin, SPI
from ssd1306 import SSD1306_SPI as ssd

''' Lolin32 configuration
sck = 14
miso = 2
mosi = 15
cs = 23
rst = 22
dc = 21
'''
# Loboris micropython
spi = SPI(1,sck=Pin(14),mosi=Pin(15),miso=Pin(2),cs=Pin(23))

''' LoPy4 configuration
dc  = 'P9' # G16
rst = 'P8' # G15
cs  = 'P12 # G28
spi = SPI(0, mode=SPI.MASTER, baudrate=1000000, polarity=0, phase=0)
'''
#oled = adafruit_ssd1306.SSD1306_SPI(128, 32, spi, dc_pin, reset_pin, cs_pin)
oled = ssd(128, 32, spi, Pin(21), Pin(22), Pin(23))


def whitescreen():
    oled.fill(1)
    oled.show()


def blankscreen():
    oled.fill(0)
    oled.show()


def messageonscreen(mesg, x, y, refresh=False):
    oled.text(mesg, x, y)
    # if refresh, then show text onscreen
    if refresh == True:
        oled.show()


import time
def demo():
    whitescreen()
    time.sleep(1)

    blankscreen()
    messageonscreen('Welkom Peter', 0,0, True)
    time.sleep(4)

    #mesg = time.strftime("%a %d %b %Y %H:%M:%S", time.localtime())
    # update date and time every second
    while True:
        time.sleep(1)
        blankscreen() # erase screen
        mesg = time.strftime("%d %b %Y", time.localtime()) # get current date
        messageonscreen(mesg, 0, 0) # store date in screenbuffer
        mesg = time.strftime("%H:%M:%S", time.localtime()) # get current time
        messageonscreen(mesg, 0, 15, True) # show screenbuffer including time and date


print(__name__, 'module loaded')
