"""

 ~ ESP-32 // Micropython ~
 buzzer.py : Simple PWM buzzer class

 Licence            : CC-NC-BY-SA 4.0
 Author             : Philippe Esling
                     <esling@ircam.fr>

"""

import time
import machine
from time import sleep_ms
from utils import midi2freq
from boards import ESP32

class Buzzer:
    
    def __init__(self):
        pass
    
    def frequency(self, freq: int = 0):
        """ Change frequency of buzzer """
        pass
        
    def volume(self, duty: float = 0):
        """ Change volume of buzzer (between 0. and 1.) """
        pass
        
    def play_note(self, midi: int, duration: int, silence: int, volume: float):
        """ Play a note for a given duration (blocking) """
        pass
        
    def play_note_async(self, midi: int, duration: int, silence: int, volume: float):
        """ Play a note (non-blocking) """
        pass
    

class BuzzerXIAO(Buzzer):
    """ Simple class for buzzer operations """
    
    def __init__(self,
            pin: int):
        super(Buzzer, self).__init__()
        self.pin = pin
        # Initialize the pin
        buzzer_pin = machine.Pin(pin, machine.Pin.OUT)
        # Initialize the PWM operation (with null)
        self.buzzer = machine.PWM(
            buzzer_pin,
            freq = 100,
            duty_u16 = 0)
        
    def frequency(self, freq: int = 0):
        """ Change frequency of buzzer """
        self.buzzer.freq(freq)
        
    def volume(self, duty: float = 0):
        """ Change volume of buzzer (between 0. and 1.) """
        self.buzzer.duty_u16(int(duty * 65535))
        
    def play_note(self,
            midi: int = 0,
            duration: int = 100,
            silence: int = 10,
            volume: float = 0.5,
        ):
        """ Play a note for a given duration (blocking) """
        hz_val = int(midi2freq(midi))
        # Set frequency and volume
        self.frequency(hz_val)
        self.volume(volume)
        # Wait for end of note
        sleep_ms(duration - silence)
        # Reset the volume
        self.volume(0)
        # Insert silence
        sleep_ms(silence)
        
    def play_note_async(self,
            midi: int = 0,
            duration: int = 100,
            silence: int = 10,
            volume: float = 0.5,
        ):
        """ Play a note (non-blocking) """
        time = Timer(0)
        time.init(
            period=1,
            mode=Timer.ONE_SHOT,
            callback=self.play_note(midi, duration, silence, volume))


def import_buzzer(
    config: dict,
    board: Board
    ):
    # Return an empty (no-op) buzzer
    if config["buzzer"] == False:
        return Buzzer()
    if (isinstance(board, ESP32)):
        buzzer = BuzzerXIAO(
            pin = board.A3)
    return buzzer