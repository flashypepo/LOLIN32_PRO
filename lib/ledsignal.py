"""
class LED based upon Signal
requires GPIO to which led is attached
    2018-0422 PePo new
"""

from micropython import const
from machine import Signal
from time import ticks_ms, sleep_ms

class LedSignal:

    def __init__(self, pin, isInvert=False):
        """ defines a Led-object attached to pin """
        self._pin = pin
        self._led = Signal(pin, invert=isInvert)
        #self._led = Pin(pin, Pin.OUT)
        self._last = 0 # used in heartbeat
        self._value = 0 # low | high signal value
        self.off()

    def on(self):
        """" set led on """
        self._led.on()
        self._value=1

    def off(self):
        """" set led off """
        self._led.off()
        self._value=0

    def toggle(self):
        """" toggle led from on to off, or vice-versa. """
        if self._value == 1:
            self.off()
        else:
            self.on()

    def _heartbeat(self):
        """" pulse led in heartbeat mode. Use it in a while-loop."""
        now = ticks_ms() # get millisecond counter
        if now - self._last > 1000:
            self.off()
            self._last = now
        elif now - self._last > 900:
            self.on()

    def heartbeat(self):
        #self._heartbeat()
        raise Exception("not implemented yet")

        # 2018-0529 doesnot work
        try:
           while True:
                self._heartbeat()
                yield()
        except:
            print('Heartbeat... done!')
            self.off() # led off

    ### properties
    @property
    def pin(self):
        return self._pin

    @property
    def value(self):
        return self._value
