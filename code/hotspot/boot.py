"""

 ~ ESP-32 // Micropython ~
 main.py : Creation of a hotspot with ESP32.
 
 This boot sequence turns the corresponding ESP32 into an Access Point (AP) through which both ESP32 and computer can connect to communicate.

 Licence            : CC-NC-BY-SA 4.0
 Author             : Philippe Esling
                     <esling@ircam.fr>

"""
import gc
import esp
import json
import time
import socket
import network
import select
from wifi import WiFi
from buzzer import import_buzzer
from screen import import_screen
from boards import ESP32C3, ESP32S3, board_dict

# Global hotspot property
ssid = "[Philoss] Hotspot"
password = "sancha4eva"
# Clean debug and garbage collect
esp.osdebug(None)
gc.collect()
# Global help values
b_id = 0 					# Board ID (Important)
b_name = "~ Hotspot v0.2 ~" # Board identifier
b_status = "Booting ..."	# Status print
read_timeout = 1000			# Time between read
alive_timeout = 10000 		# Time before considering device dead
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
# IP of the master (Ableton Live)
live_ip = ''
live_lastseen = 0
# Array of sensor boards that can connect
boards_array = [0] * 15
boards_ip = [''] * 15
boards_lastseen = [0] * 15
# Create the screen
screen = import_screen(config, board)
screen.hotspot(b_name, 'Creating ...', live_ip, boards_array)
# Create a buzzer if present
buzzer = import_buzzer(config, board)

# ---------
# Hotspot-specific code
# ---------
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password, authmode=3)
screen.hotspot(b_name, 'Activating ...', live_ip, boards_array)
# Try to activate the hotspot
while ap.active() == False:
    pass
print(ap.ifconfig())
# Create a server socket
screen.hotspot(b_name, 'Socketing ...', live_ip, boards_array)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 16841))
# s.listen(5)
screen.hotspot(b_name, 'Success.', live_ip, boards_array)
# Client accept loop
while True:
    # Wait for new message
    screen.hotspot(b_name, 'Ready.', live_ip, boards_array)
    # Create a timeout
    poller = select.poll()
    poller.register(sock, select.POLLIN)
    # Wait for available data
    res = poller.poll(read_timeout)
    # Check for alive status
    cur_time = time.ticks_ms()
    if (cur_time - live_lastseen > alive_timeout):
        live_ip = ''
    for b in range(len(boards_array)):
        if (cur_time - boards_lastseen[b] > alive_timeout):
            boards_array[b] = 0
            boards_ip[b] = ''
    # Update screen
    screen.hotspot(b_name, 'Refreshed.', live_ip, boards_array)
    if (not res):
        continue
    message, client = sock.recvfrom(2048)
    # Process message
    message = message.split(b'\x00')[0].decode('utf-8')
    client = client[0]
    print(f'Got message {message} from {client}')
    # Update corresponding status
    if (message[:4] == 'live'):
        live_ip = client
        live_lastseen = time.ticks_ms()
    else:
        board_id = int(message)
        boards_array[board_id] = 1
        boards_ip[board_id] = client
        boards_lastseen[board_id] = time.ticks_ms()
    # Update screen
    screen.hotspot(b_name, 'Updated.', live_ip, boards_array)
    

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
    