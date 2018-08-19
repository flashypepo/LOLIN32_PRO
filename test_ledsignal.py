"""
test_ledsignal.py - test class LedSignal for builtin LED
2018_0529 PePo replaced heartbeat() - it doesn't work yet
2018_0422 adopted for TTGO-ESP32_WROVER_psRAM
"""

from micropython import const
from ledsignal import LedSignal
from time import sleep_ms

# pin of builtin-led
BUILTIN_LED_PIN = const(5)

#execute
print('blinking LED on GPIO{0}'.format(BUILTIN_LED_PIN))
try:
    #led = ledsignal.LedSignal(pin=BUILTIN_LED_PIN, isInvert=True)
    led = LedSignal(pin=BUILTIN_LED_PIN, isInvert=True)
    #led.heartbeat() # doesnot work properly
    while True:
        led.on()
        sleep_ms(1000)
        led.off()
        sleep_ms(500)

except KeyboardInterrupt:
    led.off() #LED off
    print('done!')
