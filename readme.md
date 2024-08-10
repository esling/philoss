## Information sources
https://wiki.seeedstudio.com/XIAO_ESP32S3_Micropython/
https://wiki.seeedstudio.com/XIAO_ESP32C3_MicroPython/
https://wiki.seeedstudio.com/XIAO_ESP32S3_CircuitPython/
https://luvsheth.com/p/running-a-pytorch-machine-learning

### MicroPython instructions

Quick tutorial to use XIAO ESP32C3 with MicroPython.

#### Configuration

1. Install a MicroPython IDE (Mu in macOS, Thonny in Windows)
2. Update the firware using esptool
    1. Ensure that you have the `esptool` command (`pip install esptool`)
    2. Download the latest firmware for ESP32: `https://micropython.org/download/esp32c3/` or `https://micropython.org/download/ESP32_GENERIC_S3/`
    3. Flash the firmware by entering the command
```
esptool.py --chip esp32c3 --port /dev/cu.usbmodem2101  write_flash -z 0 esp32c3-usb-20230426-v1.20.0.bin
```
**Note that the port `/dev/cu.usbmodem2101` is for MacOS and may change**
**Also note that the flash file and chip name should change depending on the board**


## CircuitPython instructions

1. Download the latest firmware for ESP32: 
    1. ESP32S3 : `https://circuitpython.org/board/espressif_esp32s3_devkitc_1_n8/`
    2. ESP32C3 : `https://circuitpython.org/board/seeed_xiao_esp32c3/`
```
esptool.py --chip esp32c3 --port /dev/cu.usbmodem2101 --baud 921600 --before default_reset --after hard_reset --no-stub  write_flash --flash_mode dio --flash_freq 80m 0x0 esp32c3-usb-20230426-v1.20.0.bin
```

## Troubleshooting

### Entering bootloader mode

If something low-level fails (especially the `Failed to connect and upload to ESP32: No serial data received`), enter **bootloader mode**
**Step 1.** Press and hold the BOOT button on the XIAO ESP32S3 without releasing it.
**Step 2.** Keep the BOOT button pressed and then connect to the computer via the data cable. Release the BOOT button after connecting to the computer.
**Step 3.** Upload the Blink program to check the operation of the XIAO ESP32S3.
You can then reflash a different framework