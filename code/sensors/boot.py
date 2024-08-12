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
from udp import OSCManager
from utils import RingBuffer
from buzzer import import_buzzer
from screen import import_screen
from bare import PiezoDisc, FlexStrip
from config import boards_sensors, sensor_dict
from boards import board_dict
from led import LEDStrip

# Global help values
b_id = 1 					# Board ID (Important)
b_name = "Phi board v0.3"	# Board identifier
b_status = "Booting ..."	# Status print
b_online = False			# Online (OSC) activate
refresh_ms = 1				# Time between read
# Select one meta-config
cur_board = boards_sensors[b_id]
config = cur_board["type"] + "_expansion"
# Import corresponding JSON file from flash
with open("configs/" + config + ".json") as f:
    config = json.load(f)
    print(config)
# Type of 1st sensor is board type
b_type = cur_board["print"]
# Import WiFi JSON file from flash
with open("configs/wifi.json") as f:
    wifi_config = json.load(f)
# Select the accurate board
board = board_dict[cur_board["type"]]()
# Create a screen if present
screen = import_screen(config, board)
screen.refresh(b_name, b_type, b_status, ip_in = "", ip_out = "", values = "")
# Create a buzzer if present
buzzer = import_buzzer(config, board)
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
if (cur_board["light"]):
    strip = LEDStrip(cur_board["light"]["pin"], cur_board["light"]["n_leds"])
    strip.clear()
    # Test color wipe
    strip.rainbowWipe()
# Initialize the different sensors
buffers = [None] * len(cur_board["sensors"])
sensors = [None] * len(cur_board["sensors"])
for i, s in enumerate(cur_board["sensors"]):
    # Instatiate a buffer for each
    buffers[i] = RingBuffer(size_max = 10)
    # Create sensor object
    if (s[0] == "gyroscope"):    
        sensors[i] = sensor_dict[s[0]][0](pin_sda = s[1], pin_scl = s[2])
        continue
    print(s[0])
    print(sensor_dict[s[0]])
    sensors[i] = sensor_dict[s[0]][0](pin = s[1])
# Preprocessing function
def preprocess(buffer: RingBuffer):
    return buffer.get()[-1]
# ------------
# Main loop
# ------------
while True:
    for i in range(len(sensors)):
        raw_val = sensors[i].read()
        buffers[i].append(raw_val)
        final_val = preprocess(buffers[i])
        if (b_online):
            osc.send_osc("/sensor/" + sensor_dict[cur_board["sensors"][0]][1], [b_id, i, final_val])
        print(f'{sensors[i].__class__}:{final_val}')
        screen.refresh(b_name, b_type, "Sending.", ip_in = ip, ip_out = ip_out, values = "%.2f"%(final_val))
        time.sleep_ms(refresh_ms)