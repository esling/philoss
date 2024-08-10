"""

 ~ ESP-32 // Micropython ~
 wifi.py : Generic class for interaction with WiFi

 Licence            : CC-NC-BY-SA 4.0
 Author             : Philippe Esling
                     <esling@ircam.fr>

"""
import network
import time

class WiFi():
    """
    Generic class for using WiFi on ESP32.
    This class allows to scan for accessible networks and connect to it.
    """
    
    __authmodes = ['Open', 'WEP', 'WPA-PSK' 'WPA2-PSK4', 'WPA/WPA2-PSK', 'Unknown']
    
    def __init__(self,
            ssid: str = "",
            password: str = "",
            scan: bool = True,
            verbose: bool = True,
            config: dict = None
        ):
        if (config is not None):
            scan = config["scan"]
            verbose = config["verbose"]
            ssid = config["networks"][0]["ssid"]
            password = config["networks"][0]["password"]
        # Register the network
        self.ssid = ssid
        self.password = password
        # Create a WLAN station
        self.station = network.WLAN(network.STA_IF)
        self.station.active(True)
        # Scan for networks
        if (scan):
            self.scan()
        
    def scan(self):
        """ Function to scan for networks """
        print("Scanning for WiFi networks ...")
        for ssid, bssid, channel, RSSI, authmode, hidden in self.station.scan():
            print("* {:s}".format(ssid))
            print("   - Channel: {}".format(channel))
            print("   - RSSI: {}".format(RSSI))
            print("   - BSSID: {:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(*bssid))
            print("   - Authentication: {}".format(self.__authmodes[authmode]))
            print("   - Hidden: {}".format(hidden))
    
    def connect(self):
        while not self.station.isconnected():
            print("Connecting...")
            try:
                self.station.connect(self.ssid, self.password)
            except OSError as error:
                print(f'{error}')
                time.sleep(1)
        print("Connected!")
        print("My IP Address:", self.station.ifconfig()[0])
        print("Whole config:", self.station.ifconfig())
        
    def connected(self) -> bool:
        return self.station.isconnected()
    
    def ip(self) -> str:
        return self.station.ifconfig()[0]
    
    def mac(self) -> str:
        return self.station.config("mac")
