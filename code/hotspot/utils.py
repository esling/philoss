"""

 ~ ESP-32 // Micropython ~
 utils.py : Set of utilities for embedded classes

 Licence            : CC-NC-BY-SA 4.0
 Author             : Philippe Esling
                     <esling@ircam.fr>

"""
import math
from machine import Timer

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