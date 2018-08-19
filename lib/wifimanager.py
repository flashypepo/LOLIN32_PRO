"""
wifimanager.py - connects to Wifi networks
* Micropython: Loboris up
* static or dynamic IP
* JSON-based
2018-0529 PePo added improvements from PyCom version
2018-0520 PePo new class for Loboris uP

Format 'wificonfig.json':
{
    "STATIC_IP": "None",            # or, "145.45.16.2" for STATIC IP
    "SUBNET" : "your subnet IP",    # example: "192.168.178.0"
    "GATEWAY_IP": "your gateway IP",# example: "192.168.178.1"
    "MASKER": "your mask",          # example: "255.255.255.0",
    "SSID": "your ssid",            # example: "devices"
    "PASSWRD" : "your password",    # example WF: "devices2"
    "DNS": "8.8.8.8"                # example Google DNS
    "IDENTITY": "device id"         # kind of device id, its name
}

"""
from network import mDNS, ftp, telnet, STA_IF, WLAN
from machine import idle
import json, time
from ubinascii import hexlify

# configurations
USE_DEBUG = False   # DEBUG or not debug

class WifiManager:

    def __init__(self, jsonfile="wificonfig.json"):
        # Load configuration from config JSON file.
        # wificonfig.json contans the network settings
        # if STATIC_IP is 'None' or empty string -> use dynamic IP
        self._config = self.readjson(jsonfile)

        #create network in STAtion mode
        self._wlan = WLAN(STA_IF)


    def connect(self):
        """connect() - connects device according to network parameters in config-file."""
        #check if network is connected. If yes: return, finished
        if self._wlan.isconnected():
            if USE_DEBUG:
                print('WLAN already connected:', self._wlan.isconnected())
            # disconnect from current network
            #self.disconnect()
            return

        # activate Wifi interface
        self._wlan.active(True)
        # scan available networks for the required one
        nets = self._wlan.scan()
        for net in nets:
            ssid = net[0]
            if ssid == bytearray(self._config['SSID']): #must use bytearray!
                if USE_DEBUG:
                    print("Startup WiFi ..." + self._config['SSID'])
                # specify if static or dynamic IP is requested
                ''' 2018-0529 DEPRECATED
                is_dynamic_ip = (self._config['STATIC_IP'] == 'None') or (self._config['STATIC_IP'] == '')
                if USE_DEBUG:
                    print('Dynamic IP: {}'.format(is_dynamic_ip)) # DEBUG
                if not is_dynamic_ip:
                #'''
                if self._config['STATIC_IP'] != None:
                    if USE_DEBUG:
                        print('WifiManager::Static IP configuration')
                    # configure network for static IP
                    self._wlan.ifconfig((self._config['STATIC_IP'], self._config['MASKER'], self._config['GATEWAY_IP'], self._config['DNS']))

                # connect to SSID... either for STATIC or DYNAMIC IP
                self._wlan.connect(self._config['SSID'], self._config['PASSWRD'])
                while not self._wlan.isconnected():
                    idle() # save power while waiting
                if USE_DEBUG:
                    print("Network '{}' connection succeeded!".format(ssid))

                # start FTP and Telnet services ...
                self._startServices('myESP32', 'ESP32-WROVER', 'PePo', 'plasma')
                break

        # check connection, if not succesfull: raise exception
        if not self._wlan.active():
            raise exception('Network {0} not found.'.format(ssid))

        # returns network configuration...
        # although 'myPy.local' should work on MacOS X (Bonjour)
        return self._wlan.ifconfig()


    # wrapper for disconnecting network
    # Loboris version
    def disconnect(self):
        """disconnect() - de-activate network interface"""
        self._wlan.active(False) #loboris
        if USE_DEBUG:
            print('WifiManager::WLAN connected:', self._wlan.isconnected()) # DEBUG


    ### HELPERS ####

    def readjson(self, jsonfile):
        """readjson(file) - returns the contents of file in JSON-format"""
        with open(jsonfile, 'r') as infile:
            config = json.load(infile)
        if USE_DEBUG:
            print ('WifiManager::JSON settings: {}'.format(config))
        return config


    def print_config(self):
        """print_config() - print config data on screen."""
        for key in self._config.keys():
            print('[{0}] = {1}'.format(key, self._config[key]))


    def _startServices(self, bonjourname=None, devicename = None, user=None, passwrd=None):
        """startServices() - start Bonjour name, telnet and ftp services"""
        if (devicename == None) or (bonjourname == None) or (user == None) or (passwrd == None):
            print('WifiManager:: credentials must be specified')
            return

        # save Bonjour domain names
        self._bonjourname = bonjourname
        self._devicename = devicename

        mdns = mDNS()
        #mdns.start('myESP32', 'ESP32-WROVER')
        mdns.start(bonjourname, devicename)
        #ftp.start(user='PePo', password='plasma')
        ftp.start(user=user, password=passwrd)
        time.sleep_ms(500)
        telnet.start(user=user, password=passwrd)
        time.sleep_ms(500)
        print('FTP started:', ftp.status())
        print('Telnet started:', telnet.status())

    # change ftp and telnet credentials
    # pre-conditions:
    #        self._bonjourname != None
    #        self._devicename != None
    def change_access(self, user=None, passwrd=None):
        """change_access - change password for telnet and ftp access"""
        raise Exception("WifiManager::Not implemented yet")

        # check provided user and passwrd
        if (user == None) or (passwrd == None):
            print('WifiManager:: username and password must be specified')
            return

        # stop current services
        ftp.stop()
        telnet.stop()
        time.sleep_ms(500)

        # (re)start ftp and telnet services with new credentials
        self._startServices(self._bonjourname, self._devicename, user, passwrd)
        if USE_DEBUG:
            print('WifiManager::credentials are changed...')



    # wrapper for disabling Wifi radio
    ''' TODO check loboris up
    def deinit(self):
        """deinit() - disable Wifi radio"""
        self._wlan.deint() # pycom
        if USE_DEBUG:
            print('WifiManager::Wifi radio off')
    #'''

    # wrapper for network scan
    def scan(self):
        """scan() - Performs a network scan and returns a list
        of named tuples with (ssid, bssid, sec, channel, rssi)
        """
        return self._wlan.scan()


    #### PROPERTIES ####

    @property
    def __config(self):
        """returns config tuple"""
        return self._config


    # wrapper for wlan.isconnected()
    @property
    def isconnected(self):
        """isconnected() - returns if connected to Wifi (True) or not (False)"""
        return self._wlan.isconnected()

    @property
    def mac(self):
        """returns MAC-address of device"""
        mac = hexlify(WLAN().config('mac'),':').decode() #loboris/micropython
        #return (mac) # lower case
        return mac.upper() #upper case


# test/usage
if __name__ == "__main__":
    import wifimanager
    wifi = wifimanager.WifiManager("wificonfig.json")
    params = wifi.connect()
    print('Device IP is {0}'.format(params[0])) # device IP
    wifi.print_config()
