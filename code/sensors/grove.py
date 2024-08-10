"""

 ~ ESP-32 // Micropython ~
 grove.py : Set of Grove sensors based on our GPIO / PWM and I2C generic classes

 Licence            : CC-NC-BY-SA 4.0
 Author             : Philippe Esling
                     <esling@ircam.fr>

"""
import machine
from gpio import GPIOInputContinuous, GPIOInputDiscrete, I2C
from sensors.lis3dh import LIS3DH_I2C, RANGE_2_G, STANDARD_GRAVITY
from machine import ADC

"""
~~~~~
Rotary encoder
~~~~~
"""

class GroveRotary(GPIOInputContinuous):
    
    def __init__(self,
            pin: int):
        super(GroveRotary, self).__init__(
            pin = pin,
            attn = ADC.ATTN_11DB)
        
    def read(self,
        mode: str = "uv"):
        # read an analog value in microvolts
        val = self.adc.read_uv()
        return int(val / 20000)

"""
~~~~~
Piezo sensor
~~~~~
"""

class GrovePiezo(GPIOInputDiscrete):
    
    def __init__(self,
            pin: int):
        super(GrovePiezo, self).__init__(pin)

"""
~~~~~
Light sensor 1.2
~~~~~
"""

class GroveLight(GPIOInputContinuous):
    
    def __init__(self,
            pin: int):
        super(GroveLight, self).__init__(pin)
        
"""
~~~~~
Touch sensor
~~~~~
"""

class GroveTouch(GPIOInputContinuous):
    
    def __init__(self,
            pin: int):
        super(GroveTouch, self).__init__(pin)

"""
~~~~~
3-axis (LIS3DHTR) accelerometer
~~~~~
"""

class GroveLIS3DHTRAccelerometer(I2C):
     
    def __init__ (self,
            pin_scl: int = 6,
            pin_sda: int = 7
        ):
        super(GroveLIS3DHTRAccelerometer, self).__init__(pin_scl = pin_scl, pin_sda = pin_sda)
        # Construct object
        self.imu = LIS3DH_I2C(self.i2c)
        # Set range of accelerometer (can be 2_G, 4_G, 8_G or 16_G).
        self.imu.range = RANGE_2_G
        
    def read(self):
        # Read accelerometer values (in m / s ^ 2) as (x, y, z)
        # Divide them by 9.806 to convert to Gs.
        x, y, z = [value / STANDARD_GRAVITY for value in self.imu.acceleration]
        return (x, y, z)

"""
~~~~~
Ultrasonic ranger
~~~~~
"""
class GroveUltrasonicRanger(object):
        
    _TIMEOUT1 = 1000
    _TIMEOUT2 = 10000
    
    def __init__(self, pin):
        self.dio = machine.Pin(pin, machine.Pin.OUT)

    def _get_distance(self):
        self.dio.init(self.dio.OUT)
        self.dio.value(0)
        usleep(2)
        self.dio.value(1)
        usleep(10)
        self.dio.value(0)

        self.dio.init(self.dio.IN)

        t0 = time.time()
        count = 0
        while count < _TIMEOUT1:
            if self.dio.value():
                break
            count += 1
        if count >= _TIMEOUT1:
            return None

        t1 = time.time()
        count = 0
        while count < _TIMEOUT2:
            if not self.dio.value():
                break
            count += 1
        if count >= _TIMEOUT2:
            return None

        t2 = time.time()

        dt = int((t1 - t0) * 1000000)
        if dt > 530:
            return None

        distance = ((t2 - t1) * 1000000 / 29 / 2)    # cm

        return distance

    def get_distance(self):
        while True:
            dist = self._get_distance()
            if dist:
                return dist