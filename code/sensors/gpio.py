"""

 ~ ESP-32 // Micropython ~
 gpio.py : Generic class for GPIO sensors

 Licence            : CC-NC-BY-SA 4.0
 Author             : Philippe Esling
                     <esling@ircam.fr>

"""

from utime import localtime
from machine import Pin, ADC, PWM, I2C, SoftI2C

"""
~~~~~

Generic classes

~~~~~
"""

class Sensor():
    
    def __init__(self):
        pass
    
class InputDiscrete(Sensor):
    
    def __init__(self):
        pass
    
class OutputDiscrete(Sensor):
    
    def __init__(self):
        pass
    
class InputContinuous(Sensor):
    
    def __init__(self):
        pass
    
class OutputContinuous(Sensor):
    
    def __init__(self):
        pass

"""
~~~~~

GPIO Communication

~~~~~
"""

class GPIOOutputDiscrete(OutputDiscrete):
    
    def __init__(self,
            pin: int,
            init_value: int = None
        ):
        self.pin_id = pin
        # Create output pin
        self.pin = Pin(self.pin_id, Pin.IN)
        if (init_value is not None):
            self.pin = Pin(self.pin_id, Pin.IN, value = init_value)
        # Configure IRQ
        self.configure_irq()
        
    def value(self,
              val: int):
        self.pin.value(val)
    
    def configure_irq(self):        
        # Configure an IRQ callback
        self.pin.irq(lambda p:print(localtime()))

class GPIOInputDiscrete(InputDiscrete):
    
    def __init__(self,
            pin: int,
            pull_mode: int = None
        ):
        self.pin_id = pin
        # Create input pin
        self.pin = Pin(self.pin_id, Pin.IN, Pin.PULL_DOWN)
        # Specific pull mode (Pin.PULL_UP)
        if (pull_mode is not None):
            self.pin = Pin(self.pin_id, Pin.IN, pull_mode)
        self.pin.irq(lambda p:print(localtime()))
        
    def read(self):
        self.pin.value()
        
class GPIOOutputContinuous(OutputContinuous):
    
    def __init__(self):
        pass
    
class GPIOInputContinuous(InputContinuous):
    
    def __init__(self,
            pin: int,
            attn: int = ADC.ATTN_0DB):
        self.pin_id = pin
        # Create ADC object acting on a pin
        self.adc = ADC(self.pin_id, atten=attn)
        
    def read(self,
        mode: str = "u16"):
        if (mode == "u16"):
            # read a raw analog value in the range 0-65535
            val = self.adc.read_u16()
        else:
            # read an analog value in microvolts
            val = adc.read_uv()
        return val

"""
~~~~~

I2C Communication

~~~~~
"""

class I2C:
    
    def __init__(self,
            mode: str = "soft",
            pin_scl: int = 6,
            pin_sda: int = 7,
            frequency: int = 400 * 1e3):
        self.mode = mode
        if (mode == "absolute"):
            # Create I2C without pins
            self.i2c = I2C(freq=400000)
        elif (mode == "soft"):
            # ESP Soft pin assignment
            self.i2c = SoftI2C(
                scl=Pin(pin_scl),
                sda=Pin(pin_sda))
        else:
            raise NotImplementedError("[I2C] Unknown mode "+mode)
        # scan for peripherals, returning a list of 7-bit addresses
        # self.peripherals = self.i2c.scan()

    def writeto(self,
            address: int,
            content: bytes):
        # Write content to peripheral with 7-bit address
        self.i2c.writeto(address, content)
        
    def readfrom(self,
            address: int,
            n_bytes: int):
        # Read n_bytes bytes from peripheral with 7-bit address
        self.i2c.readfrom(address, n_bytes)
        
    
    def writeto_mem(self,
            address: int,
            mem_addr: int,
            content: bytes):
        # Write content to memory address mem_addr of peripheral with 7-bit address
        print(content)
        print(bytes(content))
        self.i2c.writeto_mem(address, mem_addr, bytes(content))
        
    def readfrom_mem(self,
            address: int,
            mem_addr: int,
            n_bytes: int):
        # Read n_bytes bytes from memory address mem_addr of peripheral with 7-bit address
        return self.i2c.readfrom_mem(address, mem_addr, n_bytes)

