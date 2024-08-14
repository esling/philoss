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
        self.data = [0] * size_max
        #self.weight = range(size_max)
        self.cur = 0
        
    def append(self, x):
        """ Append an element at the end of the buffer """
        self.data[self.cur]=x
        self.cur=(self.cur+1) % self.max
        
    def get(self):
        """ Return a list of elements from the oldest to the newest """
        return self.data[self.cur:]+self.data[:self.cur]
    
    def len(self):
        """ Length of the list """
        return self.max

#
# Set of pre-processing functions
#
def preprocess_last(buffer: RingBuffer):
    """ Just return last element """
    return buffer.get()[-1]

def preprocess_mean(buffer: RingBuffer):
    """ Mean of buffer """
    return sum(buffer.get()) / buffer.len()

def preprocess_weight(buffer: RingBuffer):
    """ Sum of buffer """
    return sum(range(buffer.len()) * buffer.get()) / sum(range(buffer.len()))

#
# Musical utility functions
#
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