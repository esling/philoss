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
from utils import freq2midi
from buzzer import import_buzzer
from screen import import_screen
from boards import ESP32C3, ESP32S3, board_dict
from grove import GroveLight, GroveTouch, GroveRotary, GrovePiezo, GroveLIS3DHTRAccelerometer
from bare import PiezoDisc, FlexStrip
from led import LEDStrip

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
    
#
# LED Strip test
#
#strip = LEDStrip(board.D7, 30)
# Test color wipe
#strip.rainbowWipe()
#strip.clear()

# <3 WORKING <3
# Initialize the rotary encoder
rotary = GroveLight(
    pin = board.A0
    )
while True:
    val = rotary.read()
    if (val > 7000):
        continue
    if (b_online):
        osc.send_osc("/sensor/piezo", [id, 1, val])
    print(val)
    screen.refresh(b_name, b_type, "Sending.", ip_in = ip, ip_out = ip_out, values = "%.2f"%(val))
    time.sleep_ms(refresh_ms)



# <3 WORKING <3
# Initialize the piezo sensor
piezo = GrovePiezo(
    pin = board.A0
    )
while True:
    time.sleep_ms(1000)
    #val = piezo.read()
    #if (val is None):
    #    print("Fak")
    #    continue
    #if (b_online):
    #    osc.send_osc("/sensor/piezo", [val])
    #print(val)
    #screen.refresh(b_name, b_type, "Sending.", ip_in = ip, ip_out = ip_out, values = "%.2f"%(val))
    #time.sleep_ms(refresh_ms)
  
# <3 WORKING <3
# Initialize the rotary encoder
rotary = GroveRotary(
    pin = board.A0
    )
while True:
    val = rotary.read()
    if (b_online):
        osc.send_osc("/control/rotary", [val])
    print(val)
    screen.refresh(b_name, b_type, "Sending.", ip_in = ip, ip_out = ip_out, values = "%.2f"%(val))
    time.sleep_ms(refresh_ms)

# <3 WORKING <3
# Initialize  the light sensor
light = GroveLight(
    pin = board.A0
    )
cur_val = -1
while True:
    val = light.read()
    smooth_val = (cur_val + val) / 2
    cur_val = val
    time.sleep_ms(refresh_ms)
    if (b_online):
        osc.send_osc("/sensor/light", [smooth_val])
    print(smooth_val)
    screen.refresh(b_name, b_type, "Sending.", ip_in = ip, ip_out = ip_out, values = "%.2f"%(smooth_val))
    gc.collect()

# <3 WORKING <3
# Initialize the touch sensor
touch = GroveTouch(
    pin = board.A1
    )
cur_val = -1
while True:
    val = touch.read()
    smooth_val = (cur_val + val) / 2
    cur_val = val
    time.sleep_ms(refresh_ms)
    if (b_online):
        osc.send_osc("/sensor/touch", [smooth_val])
    print(smooth_val)
    screen.refresh(b_name, b_type, "Sending.", ip_in = ip, ip_out = ip_out, values = "%.2f"%(smooth_val))
    gc.collect()



# <3 WORKING <3
# Perform accelerometer test
accel = GroveLIS3DHTRAccelerometer(
        pin_sda = board.SDA,
        pin_scl = board.SCL)
while True:
    (x, y, z) = accel.read()
    print("x = %0.3f G, y = %0.3f G, z = %0.3f G" % (x, y, z))
    if (b_online):
        osc.send_osc("/sensor/accel", [x, y, z])
    # Small delay to keep things responsive but give time for interrupt processing.
    time.sleep_ms(0.1)
    screen.refresh(b_name, b_type, "Sending.", ip_in = ip, ip_out = ip_out, values = "%.2f,%.2f,%.2f"%(x, y, z))



    
# <3 WORKING <3
# <3 BUT ! Value scaling is really complex
# <3 BUT ! Will require a lot of tuning ...
# Initialize the touch sensor
piezo = PiezoDisc(
    pin = board.A0
    )
cur_val = -1
while True:
    val = piezo.read()
    smooth_val = (cur_val + val) / 2
    cur_val = val
    #time.sleep_ms(1)
    if (smooth_val < 2000):
        continue
    osc.send_osc("/sensor/piezo", [smooth_val])
    print(smooth_val)
    time.sleep_ms(50)
    cur_val = piezo.read()
    gc.collect()

    
# NOOOOT WORKING
# Initialize the light sensor
flex = FlexStrip(
    pin = board.A0
    )
cur_val = -1
while True:
    val = flex.read()
    smooth_val = (cur_val + val) / 2
    cur_val = val
    time.sleep_ms(20)
    osc.send_osc("/sensor/flex", [smooth_val])
    print(smooth_val)
    gc.collect()
    
#
# NOT WORKING ZOOOOOONE
#

#
# WORKING ZOOOOOONE
#



    
    
    

