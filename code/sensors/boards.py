"""

 ~ ESP-32 // Micropython ~
 boards.py : Definition of various boards GPIO and operations

 Licence            : CC-NC-BY-SA 4.0
 Author             : Philippe Esling
                     <esling@ircam.fr>

"""
import esp
import esp32
import machine
#import vfs

class Board:

    def __init__(self):
        pass
    
    def cpu_hz(self):
        """  Get the current frequency of the CPU """
        return machine.freq()
    
    def irq_state(self,
            state: bool = True):
        """ Enable or disable IRQ """
        if (state):
            machine.enable_irq(self.irq_state)
        else:
            self.irq_state = machine.disable_irq()
            
    def idle(self):
        """ Reduce power consumption by halting execution unless IRQ """
        machine.idle()
        
    def usleep(self,
            us: int = 500):
        """
        Special function for micro sleep.
            * us is defined in _microseconds_
            * Deepsleep: may not retain RAM or state, similar to reset
        """
        if us > 1e5:
            # Sleep in miliseconds
            time.sleep_ms(int(us / 1e4))
        else:
            # Sleep in microseconds
            time.sleep_us(us)
            
            
    def sleep(self,
            ms: int = 500,
            deep: bool = False):
        """
        Stop execution for saving power.
            * Lightsleep: full RAM and state retention
            * Deepsleep: may not retain RAM or state, similar to reset
        """
        if deep:
            machine.deepsleep(ms)
        else:
            machine.lightsleep(ms)
            
    def mount_sd(self):
        """ Mount an external SD Card """
        #vfs.mount(machine.SDCard(), "/sd")
        pass
    
class ESP32(Board):
    
    def __init__(self):
        super(ESP32, self).__init__()
    
    def debug(self,
              pin: int = None):
        """ Turn off or redirect vendor O/S debugging messages """
        esp.osdebug(int)
        
    def flash_size(self):
        """ Return size of the flash memory """
        return esp.flash_size()
    
    def flash_user_start(self):
        """ Return address of user memory """
        return esp.flash_user_start()
    
    def flash_write(self,
            byte_offset,
            buffer):
        """ Write directly in the flash memory """
        return esp.flash_write(byte_offset, buffer)
    
    def flash_read(self,
            byte_offset,
            buffer):
        """ Read directly in the flash memory """
        return esp.flash_read(byte_offset, buffer)
    
class ESP32C3(ESP32):
    
    A0:		int = 2
    A1:		int = 3
    A2:		int = 4
    A3:		int = 5
    D4:		int = 6
    D5:		int = 7
    D6:		int = 21
    D7:		int = 20
    D8:		int = 8
    D9:		int = 9
    D10:	int = 10
    SCL:	int = 7
    SDA:	int = 6
    MOSI: 	int = 10
    MISO: 	int = 9
    SCK: 	int = 8
    TX: 	int = 21
    RX: 	int = 20
    
    def __init__(self):
        super(ESP32C3, self).__init__()
    
class ESP32S3(ESP32):
    
    A0:		int = 1
    A1:		int = 2
    A2:		int = 3
    A3:		int = 4
    A4:		int = 5
    A5:		int = 6
    A8:		int = 7
    A9:		int = 8
    A10:	int = 9
    D6:		int = 43
    D7:		int = 44
    SCL:	int = 6
    SDA:	int = 5
    MOSI: 	int = 9
    MISO: 	int = 8
    SCK: 	int = 7
    TX: 	int = 43
    RX: 	int = 44
    
    def __init__(self):
        super(ESP32S3, self).__init__()

board_dict = {
    'esp32':	ESP32,
    'esp32c3': 	ESP32C3,
    'esp32s3': 	ESP32S3,
}