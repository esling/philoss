"""

 ~ ESP-32 // Micropython ~
 utils.py : Set of utilities for embedded classes

 Licence            : CC-NC-BY-SA 4.0
 Author             : Philippe Esling
                     <esling@ircam.fr>

"""
import math
from machine import Timer

#
# Homemade ring buffer implementation
#
class RingBuffer:
    def __init__(self, size_max):
        self.max = size_max
        self.data = []
    def append(self,x):
        """append an element at the end of the buffer"""
        self.data.append(x)
        if len(self.data) == self.max:
            self.cur=0
            self.__class__ = RingBufferFull
    def get(self):
        """ return a list of elements from the oldest to the newest"""
        return self.data


class RingBufferFull:
    def __init__(self,n):
        raise "you should use RingBuffer"
    def append(self,x):     
        self.data[self.cur]=x
        self.cur=(self.cur+1) % self.max
    def get(self):
        return self.data[self.cur:]+self.data[:self.cur]

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