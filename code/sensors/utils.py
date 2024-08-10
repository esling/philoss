"""

 ~ ESP-32 // Micropython ~
 utils.py : Set of utilities for embedded classes

 Licence            : CC-NC-BY-SA 4.0
 Author             : Philippe Esling
                     <esling@ircam.fr>

"""
import math
from machine import Timer

# One-shot firing after 5 seconds (ID 0)
#tim0 = Timer(0)
#tim0.init(period=5000, mode=Timer.ONE_SHOT, callback=lambda t:print(0))

# Periodic every 2 seconds (ID 1)
#tim1 = Timer(1)
#tim1.init(period=2000, mode=Timer.PERIODIC, callback=lambda t:print(1))

# periodic at 1kHz (ID 2)
# tim2 = Timer(2)
# def mycallback(t):
# 	pass
# tim.init(mode=Timer.PERIODIC, freq=1000, callback=mycallback)
# Stop the timer
# tim.deinit()

def freq2midi(
        freq: float
    ):
    """ Given a frequency in Hz, returns its MIDI pitch number. """
    MIDI_A4 = 69   # MIDI Pitch number
    FREQ_A4 = 440. # Hz
    return int(12 * (math.log2(freq) - math.log2(FREQ_A4)) + MIDI_A4)

def midi2freq(
        midi: int
    ):
    """ Given a MIDI pitch number, return its frequency in Hz. """
    FREQ_A4 = 440. # Hz
    return (FREQ_A4 / 32) * (2. ** ((float(midi) - 9.) / 12.));