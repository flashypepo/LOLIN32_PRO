# main.py
print('main started...')

import time

# 2018-0728 rainbow on connected neopixel-matrix (Pin 22)
from neomatrix import rainbow
from neomatrix import np
rainbow(loops=240)
time.sleep(1)
np.clear()
print('main finished.')
