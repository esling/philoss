"""

 ~ ESP-32 // Micropython ~
 screen.py : Interaction with a screen

 Licence            : CC-NC-BY-SA 4.0
 Author             : Philippe Esling
                     <esling@ircam.fr>

"""
import time
import math
import framebuf
import ssd1306
from boards import Board, ESP32
from machine import Pin, SoftI2C

class Screen:
    
    def __init__(self,
            contrast: int = 255,
            invert: int = 1,
            rotate: bool = True):
        self.contrast = contrast
        self.invert = invert
        self.rotate = rotate
    
    def on(self):
        """ Power on the screen """
        pass
    
    def off(self):
        """ Power off the screen """
        pass
    
    def clear(self):
        """ Clear the screen """
        pass
    
    def show(self):
        """ Refresh content on screen """
        pass
        
    def pixel(x: int, y: int, color: int = 1):
        """ Draw a pixel at (x, y) """
        pass
        
    def line(x1: int, y1: int, x2: int, y2: int, color: int = 1):
        """ Draw a line between (x1, y1) and (x2, y2) """ 
        pass 
        
    def rect(x1: int, y1: int, x2: int, y2: int, color: int = 1):
        """ Draw a rectangle (outline) between (x1, y1) and (x2, y2) """  
        pass
        
    def fill_rect(x1: int, y1: int, x2: int, y2: int, color: int = 1):
        """ Draw a rectangle (filled) between (x1, y1) and (x2, y2) """   
        pass
        
    def text(txt: str, x: int, y: int, color: int = 1):
        """ Draw some text (txt) at (x, y) """
        pass

    def scroll(x: int, dir: int = 0):
        """ Scroll x pixels to the (0: right, 1: left) """
        pass
    
    def add_text(self, val: str):
        """ Add text at the end of the current content """
        pass

    
class OLEDSSD1306(Screen):
    
    def __init__(self,
            pin_scl: int,
            pin_sda: int,
            contrast: int = 127,
            invert: int = 0,
            rotate: bool = True
            ):
        super(OLEDSSD1306, self).__init__(contrast, invert, rotate)
        # ESP Pin assignment
        self.i2c = SoftI2C(
            scl=Pin(pin_scl),
            sda=Pin(pin_sda))
        # SSD1306 properties
        self.oled_width = 128
        self.oled_height = 64
        # Initialize I2C
        self.oled = ssd1306.SSD1306_I2C(
            self.oled_width,
            self.oled_height,
            self.i2c)
        # Setup parameters
        self.oled.contrast(self.contrast)
        self.oled.invert(self.invert)
        self.oled.rotate(self.rotate)
        # Content start position
        self.content_x = 0
        self.content_y = 0
    
    def on(self):
        """ Power on the screen """
        self.oled.poweron()
    
    def off(self):
        """ Power off the screen """
        self.oled.poweroff()
        
    def clear(self):
        """ Clear the screen """
        self.oled.fill(0)
        self.content_x = 0
        self.content_y = 0
        
    def show():
        """ Refresh content on screen """
        self.oled.show()
        
    def pixel(x: int, y: int, color: int = 1):
        """ Draw a pixel at (x, y) """
        self.oled.pixel(x, y, color)
        
    def line(x1: int, y1: int, x2: int, y2: int, color: int = 1):
        """ Draw a line between (x1, y1) and (x2, y2) """    
        self.oled.line(x1, y1, x2, y2, color)
        
    def rect(x1: int, y1: int, x2: int, y2: int, color: int = 1):
        """ Draw a rectangle (outline) between (x1, y1) and (x2, y2) """   
        self.oled.rect(x1, y1, x2, y2, color)
        
    def fill_rect(x1: int, y1: int, x2: int, y2: int, color: int = 1):
        """ Draw a rectangle (filled) between (x1, y1) and (x2, y2) """   
        self.oled.fill_rect(x1, y1, x2, y2, color)
        
    def text(txt: str, x: int, y: int, color: int = 1):
        """ Draw some text (txt) at (x, y) """
        self.oled.text(txt, x, y, color)

    def scroll(x: int, dir: int = 0):
        """ Scroll x pixels to the (0: right, 1: left) """
        self.oled.scroll(x, dir)
    
    def add_text(self, val: str):
        """ Add text at the end of the current content """
        self.oled.text(val, self.content_x, self.content_y, 1)
        self.content_y += 10
        self.oled.show()
    
    def draw_buffer(self):
        # Draw another FrameBuffer on top of the current one at the given coordinates
        fbuf = framebuf.FrameBuffer(bytearray(8 * 8 * 1), 8, 8, framebuf.MONO_VLSB)
        fbuf.line(0, 0, 7, 7, 1)
        self.oled.blit(fbuf, 10, 10, 0)           # draw on top at x=10, y=10, key=0
        self.oled.show()
        
    def hotspot(
        self,
        name: str = "Board",
        status: str = 'Idle',
        master: str = '',
        boards = None,
    ):
        statuses = [' ', 'x']
        str_boards = ''
        for b in boards:
            str_boards += f'[{statuses[b]}]'
        live_status = statuses[(len(master) > 0)]
        self.clear()
        self.oled.text(name, self.content_x, 0, 1)
        self.oled.text(f"|{live_status}| {master}", self.content_x, 10, 1)
        self.oled.text(str_boards[:15], self.content_x, 20, 1)
        self.oled.text(str_boards[15:30], self.content_x, 30, 1)
        self.oled.text(str_boards[30:], self.content_x, 40, 1)
        self.oled.text("_________________", self.content_x, 45, 1)
        self.oled.text("" + status, self.content_x, 57, 1)
        self.content_y = 60
        self.oled.show()


screen_dict = {
    'oled': 	OLEDSSD1306
}

def import_screen(
    config: dict,
    board: Board
    ):
    # Return an empty (no-op) screen
    if config["screen"] == 0:
        return Screen()
    if (isinstance(board, ESP32)):
        screen = OLEDSSD1306(
            pin_scl = board.SCL,
            pin_sda = board.SDA)
    return screen
    