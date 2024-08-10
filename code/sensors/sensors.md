# List of sensors

## Bare sensors

* Piezoelectric disc
    - Working (past version)
* Bending strip
    - Working (past version)
* Octocoupler
    - Working (past version)
* Touch strip
    - Untested

## Grove sensors

* Light sensor v1.2
A light sensor is based on a photo-resistor (light-dependent resistor) to detect the intensity of light. 
The resistance of photo-resistor decreases when the intensity of light increases. 
The output signal is analog value, the brighter the light is, the larger the value.
    - Uses a single ADC GPIO pin (easy to override)
    - Outputs a continuous value
    
* Mini-PIR sensor
* 3-Axis digital accelerometer (LIS3DHTR)
3-Axis Digital Accelerometer is based on the LIS3DHTR chip which provides multiple ranges and interfaces selection. 
This accelerometer can support I2C, SPI, and ADC GPIO interfaces, which means you can choose any way to connect. 
Besides, this accelerometer can also monitor the surrounding temperature to tune the error caused by it.
I2C address	Default 0x19, can be changed to 0x18 when connecting SDO Pin with GND

* Temperature & humidity v2.1
* Analog microphone v1.0
* Rotary encoder
* Ultrasonic distance v2.0
* Infrared receiver v1.2
* Touch sensor
* Moisture sensor

### Output

* 3-color waterproof LED strip
* Servomotor