"""
rtc_sync - synchronize with NTTPserver
pre-condition: device connected to Wifi
2018-0529 pepo added timerecord()
2018-0520 pepo new, extracted from ws1.py
"""
from machine import RTC
from time import sleep_ms, localtime, strftime

# real-time clock
rtc = RTC()

# test if rtc needs to be synchronized
if rtc.now()[0] < 1975:
    # get the time from NTTP-server
    rtc.ntp_sync(server='nl.pool.ntp.org', tz='CET-1CEST,M3.5.0,M10.5.0/3')
    sleep_ms(500) # small delay - trial and error

#print('rtc.now:', rtc.now())
''' 2019-0529 DEPRECATED
year = rtc.now()[0]
month = rtc.now()[1]
day = rtc.now()[2]
hour = rtc.now()[3]
min = rtc.now()[4]
secs = rtc.now()[5]
print("It's {0}:{1} at {2}-{3}-{4}".format(hour, min, year,month,day))
#'''
def timerecord():
    return strftime("%a %d %b %Y %H:%M:%S", localtime())

print("It's", timerecord())
