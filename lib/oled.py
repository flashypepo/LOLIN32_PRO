"""
oled - an abstraction for an OLED display

2018-0529 PePo first version, Loboris, i2c-OLED
pre-condition: i2c is initialized
"""
import machine
import ssd1306
from utils import readjson

USE_DEBUG = False # to print debug-messages or not

class OLED():

    def __init__(self, wSize, hSize, i2c, addrOled):

        if USE_DEBUG:
            print('Scan i2c bus...')

        # collect i2c-devices
        devices = i2c.scan()
        if len(devices) == 0:
          #print("No i2c device !")
          raise Exception("No i2c device!")

        if USE_DEBUG:
            print('i2c devices found:',len(devices))

        # look for OLED display in i2c...
        for device in devices:
            if device == addrOled:
                self._oledIsConnected = True
            #if device == addrBME280:
            #    bmeIsConnected = True
            if USE_DEBUG:
                print("Device", device)

        if not self._oledIsConnected:
            raise Exception("OLED is not connected")

        # init OLED
        self._oled = ssd1306.SSD1306_I2C(wSize, hSize, i2c)
        self.clear(False) # clear OLED buffer

    # clear OLED
    # refresh = False: only buffer.
    # refresh = True:  screen too.
    def clear(self, refresh=False):
        self._oled.fill(0)
        if refresh:
            self._oled.show()

    # oled.showHeader('DHT22', 0, y)
    def showHeader(self, msg, kol, row, refresh=False):
        self._oled.text(msg, kol, row)
        if refresh == True:
            self._oled.show()

    # show a message on screen (x,y)
    # pre-condition: OLED is connected
    # Note: (partial)clearing oled is never done and must be done elsewhere
    def message(self, mesg, x, y, refresh=False):
        self._oled.text(mesg, x, y)
        # if refresh, then show text onscreen
        if refresh == True:
            self._oled.show()

    # display icon at position (x,y)
    # 2018-0529 not tested yet
    def show_icon(self, icon, dx=0, dy=0):
        """display_icon(icon): display an icon (matrix) on display """
        for y, row in enumerate(icon):
            y += dy # offset
            for x, c in enumerate(row):
                x += dx # offset
                self._oled.pixel(x, y, c)
        self._oled.show()


    @property
    def isconnected(self):
        return self._oledIsConnected == True

    @property
    def oled_screen(self):
        return self._oled
