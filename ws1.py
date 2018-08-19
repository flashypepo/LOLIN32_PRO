"""
ws1.py

ESP32 websocket server based upon
https://www.rototron.info/raspberry-pi-esp32-micropython-websockets-tutorial/

2018-0514 PePo new, uses the BME280 temperature sensor (I2C)
"""
import machine
from machine import I2C, RTC, Timer
from microWebSrv import MicroWebSrv
import json
from time import sleep
import bme280  # temperature sensor

# setup BME280 temperature sensor, I2C
i2c = machine.I2C(0, sda=21, scl=22)
bme = bme280.BME280(i2c=i2c)

# real-time clock
rtc = RTC()
rtc.ntp_sync(server='nl.pool.ntp.org', tz='CET-1CEST,M3.5.0,M10.5.0/3')

# hardware timer
tm = Timer(0)

def cb_receive_text(webSocket, msg):
    print("WS RECV TEXT : %s"% msg)
    webSocket.SendText("REPLY for %s"% msg)

def cb_receive_binary(webSocket, data):
    print("WS RECV DATA : %s"% data)

def cb_closed(webSocket):
    tm.deinit() # dispose of Timer
    print("WS CLOSED")

# callback at each timer event
def cb_timer(timer, websocket):
    dict = {} # store data in dict
    dict['temp'] = bme.values[0]
    print(dict['temp'])
    dict['pressure'] = bme.values[1]
    print(dict['pressure'])
    dict['humidity'] = bme.values[2]
    print(dict['humidity'])
    dict['internal'] = machine.internal_temp()[1] #ESP32 temperature sensor
    dict['time'] = rtc.now() #current time
    websocket.SendText(json.dumps(dict)) #JSON format

def cb_accept_ws(webSocket, httpClient):
    print("WS ACCEPT")
    webSocket.RecvTextCallback = cb_receive_text
    webSocket.RecvBinaryCallback = cb_receive_binary
    webSocket.ClosedCallback = cb_closed
    # use lambda to inject websocket:
    cb = lambda timer: cb_timer(timer, webSocket)
    tm.init(periode=3000, callback=cb) # init and starts timer to poll temperature

mws = MicroWebSrv() #TCP port 80, files in /flash/www
mws.MaxWebSocketRecvLen = 256 #default 1024
mws.WebSocketThreaded = True # use threads
mws.WebSocketStackSize = 4096
mws.AcceptWebSocketCallback = cb_accept_ws
mws.Start(threaded=False) #blocking call (CTRL-C to exit)

# cleaning up
print('Cleaning up and exiting.')
mws.Stop()
tm.deinit()
rtc.clear()
#TODO: bme.deinit()
i2c.deinit()
