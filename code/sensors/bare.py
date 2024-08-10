"""

 ~ ESP-32 // Micropython ~
 grove.py : Set of Grove sensors based on our GPIO / PWM and I2C generic classes

 Licence            : CC-NC-BY-SA 4.0
 Author             : Philippe Esling
                     <esling@ircam.fr>

"""
import machine
from gpio import GPIOInputContinuous, GPIOInputDiscrete

"""
~~~~~
Piezo-electric discs
~~~~~
"""

class PiezoDisc(GPIOInputContinuous):
    
    def __init__(self,
            pin: int):
        super(PiezoDisc, self).__init__(pin)

"""
~~~~~
Flex sensor
~~~~~
"""

class FlexStrip(GPIOInputContinuous):
    
    def __init__(self,
            pin: int):
        super(FlexStrip, self).__init__(pin)
        