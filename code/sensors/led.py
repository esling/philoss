"""

 ~ ESP-32 // Micropython ~
 led.py : Generic class for LED strip output

 Licence            : CC-NC-BY-SA 4.0
 Author             : Philippe Esling
                     <esling@ircam.fr>

"""
import time
import machine
import neopixel

class LEDStrip():
    
    def __init__(self,
            pin: int,
            n_leds: int):
        self.pin = pin
        self.n_leds = n_leds
        # Configure the LED strip
        p = machine.Pin(pin)
        self.strip = neopixel.NeoPixel(p, n_leds)
        
    def set_color(self,
            index: int,
            color: Tuple[int],
            update: bool = True):
        self.strip[index] = color
        if (update):
            self.strip.write()
            
    def clear(self):
        for i in range(self.n_leds):
            self.strip[i] = (0, 0, 0)
        self.strip.write()

    #
    # Animations
    #
    def colorWipe(self,
            color: int = (255, 0, 0),
            wait_ms: int = 50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.n_leds):
            self.set_color(i, color)
            time.sleep_ms(wait_ms)
            
    
    def rainbowWipe(self,
            wait_ms: int = 50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.n_leds):
            self.set_color(i, self.wheel(int(i * 256 / self.n_leds)))
            time.sleep_ms(wait_ms)
        for i in range(self.n_leds):
            self.set_color(i, (0, 0, 0))
            time.sleep_ms(wait_ms)

    def theaterChase(self,
            color: List[int] = (255, 0, 0),
            wait_ms: int = 50,
            iterations: int = 10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.n_leds, 3):
                    self.set_color(i + q, color, False)
                self.strip.write()
                time.sleep_ms(wait_ms)
                for i in range(0, self.n_leds, 3):
                    self.set_color(i + q, (0, 0, 0), False)

    def wheel(self,
            pos: int):
        """ Generate rainbow colors across 0-255 positions. """
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)

    def rainbow(self,
            wait_ms: int = 20,
            iterations: int = 1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * iterations):
            for i in range(self.n_leds):
                self.set_color(i, self.wheel((i+j) & 255), False)
            self.strip.write()
            time.sleep_ms(wait_ms)

    def rainbowCycle(self,
            wait_ms: int = 20,
            iterations: int = 5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256 * iterations):
            for i in range(self.n_leds):
                self.set_color(i, self.wheel((int(i * 256 / self.n_leds) + j) & 255), False)
            self.strip.write()
            time.sleep_ms(wait_ms)

    def theaterChaseRainbow(self,
            wait_ms: int = 50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.n_leds, 3):
                    self.set_color(i + q, self.wheel((i+j) % 255), False)
                self.strip.write()
                time.sleep_ms(wait_ms)
                for i in range(0, self.n_leds, 3):
                    self.set_color(i + q, (0, 0, 0), False)
