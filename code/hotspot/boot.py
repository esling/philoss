"""

 ~ ESP-32 // Micropython ~
 main.py : Creation of an interaction with ESP32

 Licence            : CC-NC-BY-SA 4.0
 Author             : Philippe Esling
                     <esling@ircam.fr>

"""
import gc
import json
import machine
import utime as time
from wifi import WiFi
from buzzer import import_buzzer
from screen import import_screen
from boards import ESP32C3, ESP32S3, board_dict

# Global help values
b_id = 1 					# Board ID (Important)
b_name = "Phi board v0.3"	# Board identifier
b_status = "Booting ..."	# Status print
b_online = False			# Online (OSC) activate
refresh_ms = 0				# Time between read
# Select one meta-config
config = "esp32c3_expansion"
# Import corresponding JSON file from flash
with open("configs/" + config + ".json") as f:
    config = json.load(f)
    print(config)
# Type of 1st sensor is board type
b_type = config["sensors"][0]["type"]
# Import WiFi JSON file from flash
with open("configs/wifi.json") as f:
    wifi_config = json.load(f)
# Select the accurate board
board = board_dict[config["board"]]()
# Create a screen if present
screen = import_screen(config, board)
screen.refresh(b_name, b_type, b_status, ip_in = "", ip_out = "", values = "")
# Create a buzzer if present
print("Buzz")
buzzer = import_buzzer(config, board)
print("Buzz")
# Initialize network settings
if (b_online):
    screen.refresh(b_name, b_type, "Connecting ...")
    wifi = WiFi(
        ssid = wifi_config["networks"][0]["ssid"],
        password = wifi_config["networks"][0]["password"],
        scan = False)
    # Connect to the WiFi
    wifi.connect()
    # Retrieve the IP
    ip = wifi.ip()
    screen.refresh(b_name, b_type, "Connected.", ip_in = ip, ip_out = "", values = "")
    # Infer board IP
    board_id = ip.split(".")[-1]
    # Create a UDP/OSC client and server
    screen.refresh(b_name, b_type, "OSC Discover ...", ip_in = ip, ip_out = "", values = "")
    osc = OSCManager(
        host = config["osc"]["host"],
        in_port = config["osc"]["in_port"],
        out_port = config["osc"]["out_port"],
        bc_port = config["osc"]["bc_port"],
        discovery = config["discovery"])
    ip_out = osc.host
    screen.refresh(b_name, b_type, "OSC Found.", ip_in = ip, ip_out = ip_out, values = "")
else:
    ip = " Off."
    ip_out = " Off."
    
# Initialize the different sensors
for s in config["sensors"]:
    print(s)
    