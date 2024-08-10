"""

 ~ ESP-32 // Micropython ~
 lis3dhtr.py : This code is meant for the LIS3DHTR_I2CS I2C, especially for the Grove accelerometer.
 Here, all we use it for is to keep a static list of all the I2C registers and other module constants

 Licence            : CC-NC-BY-SA 4.0
 Author             : Philippe Esling
                     <esling@ircam.fr>

"""
import time

class LIS3DHTR:
    
    # I2C address of the device
    DEFAULT_ADDRESS 	= 0x19
    
    # LIS3DHTR Register Map
    REG_WHOAMI			= 0x0F # Who Am I Register
    REG_CTRL1			= 0x20 # Control Register-1
    REG_CTRL2			= 0x21 # Control Register-2
    REG_CTRL3			= 0x22 # Control Register-3
    REG_CTRL4			= 0x23 # Control Register-4
    REG_CTRL5			= 0x24 # Control Register-5
    REG_CTRL6			= 0x25 # Control Register-6
    REG_REFERENCE		= 0x26 # Reference
    REG_STATUS			= 0x27 # Status Register
    REG_OUT_X_L			= 0x28 # X-Axis LSB
    REG_OUT_X_H			= 0x29 # X-Axis MSB
    REG_OUT_Y_L			= 0x2A # Y-Axis LSB
    REG_OUT_Y_H			= 0x2B # Y-Axis MSB
    REG_OUT_Z_L			= 0x2C # Z-Axis LSB
    REG_OUT_Z_H			= 0x2D # Z-Axis MSB
    
    # Accelerometer datarate configuration
    ACCL_DR_PD			= 0x00 # Power down mode
    ACCL_DR_1			= 0x10 # ODR = 1 Hz
    ACCL_DR_10			= 0x20 # ODR = 10 Hz
    ACCL_DR_25			= 0x30 # ODR = 25 Hz
    ACCL_DR_50			= 0x40 # ODR = 50 Hz
    ACCL_DR_100			= 0x50 # ODR = 100 Hz
    ACCL_DR_200			= 0x60 # ODR = 200 Hz
    ACCL_DR_400			= 0x70 # ODR = 400 Hz
    ACCL_DR_1620		= 0x80 # ODR = 1.620 KHz
    ACCL_DR_1344		= 0x90 # ODR = 1.344 KHz
    
    # Accl Data update & Axis configuration
    ACCL_LPEN			= 0x00 # Normal Mode, Axis disabled
    ACCL_XAXIS			= 0x04 # X-Axis enabled
    ACCL_YAXIS			= 0x02 # Y-Axis enabled
    ACCL_ZAXIS			= 0x01 # Z-Axis enabled
    
    # Acceleration Full-scale selection
    BDU_CONT			= 0x00 # Continuous update, Normal Mode, 4-Wire Interface
    BDU_NOT_CONT		= 0x80 # Output registers not updated until MSB and LSB reading
    ACCL_BLE_MSB		= 0x40 # MSB first
    ACCL_RANGE_16G		= 0x30 # Full scale = +/-16g
    ACCL_RANGE_8G		= 0x20 # Full scale = +/-8g
    ACCL_RANGE_4G		= 0x10 # Full scale = +/-4g
    ACCL_RANGE_2G		= 0x00 # Full scale = +/-2g, LSB first
    HR_DS				= 0x00 # High-Resolution Disabled
    HR_EN				= 0x08 # High-Resolution Enabled
    ST_0 				= 0x02 # Self Test 0
    ST_1				= 0x04 # Self Test 1
    SIM_3				= 0x01 # 3-Wire Interface

