"""
read sensor-values from DHT-sensor
2018-0227 PePo new for loboris uP
"""
from machine import Pin, DHT
from time import sleep

class DHTSensor:
    'DHTSensor class for loboris uP'

    def __init__(self, sensor_pin, sensor_type):
        """ pin = pin number of DHT-sensor
            type = type of sensor, DHT11 | DHT2x
        """
        self._dht_pin = Pin(sensor_pin)
        self._dht_type = sensor_type
        self._dht = DHT(self._dht_pin, self._dht_type)

    def read(self):
        """ read sensor, returns tuple (temperature
        and humidity) when success, else return None"""
        success, temperature, humidity = self._dht.read()
        if not success:
            return (None, None)
        else:
            return (temperature, humidity)


    @property
    def sensor(self):
        """ returns sensor object"""
        return self._dht


    @property
    def pin(self):
        """ returns Pin of sensor"""
        return self._dht_pin


    @property
    def type(self):
        """ returns type of sensor (DHT11 | DHT2X)"""
        if self._dht_type is DHT.DHT11:
            return 'DHT11'
        if self._dht_type is DHT.DHT2X:
            return 'DHT2X'

# usage:
if __name__ == "__main__":
    import machine, dhtsensor, time
    dht = dhtsensor.DHTsensor(15, machine.DHT.DHT2X)
    #def run(self, dt=10):
    print('DHT type:', dht.type)
    print('Sensor:', dht.sensor)
    print('Sensor-pin:', dht.pin)
    while True:
        t, h = self.read()
        print('t={0} C, h={1} % RH'.format(t, int(h)))
        sleep(5)
    #dht.run(5)
