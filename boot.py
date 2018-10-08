# This file is executed on every boot (including wake-boot from deepsleep)
import sys
sys.path[1] = '/flash/lib'

import gc
gc.collect()
print('memory:', gc.mem_free())
