"""

 ~ ESP-32 // Micropython ~
 main.py : Creation of an interaction with ESP32

 Licence            : CC-NC-BY-SA 4.0
 Author             : Philippe Esling
                     <esling@ircam.fr>

"""
import gc
import json
import socket
import machine
import utime as time
from wifi import WiFi
from udp import OSCManager
from utils import RingBuffer
from buzzer import import_buzzer
from screen import import_screen
from bare import PiezoDisc, FlexStrip
from config import boards_sensors, sensor_dict, sensor_normalize
from boards import board_dict
from led import LEDStrip

# Safety reset
gc.collect()
# Global config values
b_id = 1 					# Board ID (Important)
b_name = "[Phi board v0.3"	# Board identifier
b_status = "Booting ..."	# Status print
b_online = False			# Online (OSC) activate
refresh_ms = 5				# Global pause time between read
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
    # Create a keep alive socket (hotspot)
    alive_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    alive_dest = ('192.168.4.1', 16841)
    # Send an alive message
    alive_sock.sendto(str(b_id).encode(), alive_dest)
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
    # Send a connection message to live
    board_type = cur_board["type"]
    sensors_list = " ".join([f"{i}:{t[0]}" for i, t in enumerate(cur_board["sensors"])])
    osc.send_osc("/connect", [b_id, board_type, sensors_list])
else:
    ip = " Off."
    ip_out = " Off."
# Handle potential LED strip
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
    print(f'Init:{sensor_dict[s[0]]}')
    # Create sensor object
    if (s[0] == "gyroscope"):
        sensors[i] = sensor_dict[s[0]][0](pin_sda = s[1], pin_scl = s[2])
        continue
    sensors[i] = sensor_dict[s[0]][0](pin = s[1])
# Clean garbage
gc.collect()
# ------------
# Main loop
# ------------
while True:
    values = [0] * len(sensors)
    # Parse through all sensors
    for i in range(len(sensors)):
        # Raw reading
        raw_val = sensors[i].read()
        # Fill the buffer
        buffers[i].append(raw_val)
        # Apply sensor-specific preprocessing function
        proc_val = sensor_dict[cur_board["sensors"][i][0]][2](buffers[i])
        final_val = sensor_normalize(proc_val, cur_board["sensors"][i][0])
        # Thresholding value for accounting the value
        if (final_val <= 0.):
            continue
        if (b_online):
            # Send current value to OSC
            osc.send_osc("/sensor/" + sensor_dict[cur_board["sensors"][i][0]][1], [b_id, i, final_val])
        print(f'{str(sensors[i].__class__)[13:-2]:14s}: {final_val:3.3f}')
    # Prepare output value
    screen.refresh(b_name, b_type, "Sending.", ip_in = ip, ip_out = ip_out, values = "%.2f"%(final_val))
    time.sleep_ms(refresh_ms)
    #gc.collect()
    if (b_online):
        # Send the keep-alive message
        alive_sock.sendto(str(b_id).encode(), alive_dest)
