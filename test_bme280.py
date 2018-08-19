'''
  test a MBE280/BMP280 temperature  sensor
  pin sensor  ESP32-WROVER
  SCL         GPIO21
  SDA         GPIO22
  VIN         3.3V
  GND         GND

  2018-0514 ESP32-WROVER, loboris up 2018-0510

#'''
from micropython import const
import machine
import time
import json
import bme280   #required in lib-folder

# helper function: Celsius to Fahrenheit
# 2018-0402 requires changes in class BME280 - stored somewhere?

def fahrenheit(celsius):
    return (celsius * 9/5) + 32

# make i2c object
SCL_PIN = const(21) #compile constant
SDA_PIN = const(22)

#Loboris wiki:
i2c = machine.I2C(0, sda=21, scl=22)
#debug:
print('i2c.scan: ', i2c.scan())

#BME280 sensor object
bme = bme280.BME280(i2c=i2c)

def sensor_data():
    dict = {} # store data in dict
    dict['temp'] = bme.values[0]
    #print(dict['temp'])
    dict['pressure'] = bme.values[1]
    #print(dict['pressure'])
    dict['humidity'] = bme.values[2]
    #print(dict['humidity'])
    dict['internal'] = machine.internal_temp()[1] #ESP32 temperature sensor
    return json.dumps(dict) #JSON format

# run sensor reading, Ctrl-C to abort
def run(dt=2.0):
    try:
        while True:
            print('BME280 values: ', bme.values)
            print('JSON:', sensor_data())
            time.sleep(dt) #wait > s, see datasheet
    except:
        print('done')

run(5) # 5 secs
