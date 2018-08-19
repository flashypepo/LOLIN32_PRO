"""
generic class LED
requires GPIO to which led is attached
2018-0313 PePo new

2018-0313: move to application level
    LED_PIN: uncomment the proper connect LED
    TODO: make configuration file
    LED_PIN = const(22) # builtin LED of Lolin32 Lite
    LED_PIN = const(19) # LED, Lolin32 Lite
    LED_PIN = const(2) # LED, Adafruit Huzzah ESP8266
"""

from micropython import const
from machine import Pin
from time import ticks_ms

class Led:

    def __init__(self, pin):
        """ defines a Led-object attached to pin """
        self._pin = pin
        self._led = Pin(pin, Pin.OUT)
        self._last = 0 # used in heartbeat

    def on(self):
        """" set led on """
        self._led.value(1)

    def off(self):
        """" set led off """
        self._led.value(0)

    def toggle(self):
        """" toggle led from on to off, or vice-versa. """
        self._led.value(not self._led.value())

    def _heartbeat(self):
        """" pulse led in heartbeat mode. Use it in a while-loop."""
        now = ticks_ms() # get millisecond counter
        if now - self._last > 1000:
            self._led.value(0)
            self._last = now
        elif now - self._last > 900:
            self._led.value(1)

    def heartbeat(self):
        #self._heartbeat()
        try:
           while True:
                self._heartbeat()
        except:
            print('Heartbeat... done!')
            self.off() # led off

    ### properties
    @property
    def pin(self):
        return self._pin

    @property
    def value(self):
        return self._led.value()
