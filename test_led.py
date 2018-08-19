"""
test_led.py - test for builtin LED
2018_0422 adopted for TTGO-ESP32_WROVER_psRAM
2018_0324 OOP-versie with lib/led,
"""
import led

# pin of builtin-led
BUILTIN_LED_PIN = 5

#execute
print('blinking LED on GPIO{0}'.format(BUILTIN_LED_PIN))
try:
    builtinLed = led.Led(BUILTIN_LED_PIN)
    builtinLed.heartbeat()

except KeyboardInterrupt:
    builtinLed.off() #LED off
    print('done!')
