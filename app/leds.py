import board
import neopixel
import time
import colorsys
from visual import Frame

pixels = neopixel.NeoPixel(board.D18, 50, brightness=1, auto_write=False)


translate_pixel = {
        0: 11,  1: 12,  2: 35,  3: 36,
        4: 10,  5: 13,  6: 34,  7: 37,
        8: 9,   9: 14, 10: 33, 11: 38,
        12: 8, 13: 15, 14: 32, 15: 39,
        16: 7, 17: 16, 18: 31, 19: 40,
        20: 6, 21: 17, 22: 30, 23: 41,
        24: 5, 25: 18, 26: 29, 27: 42,
        28: 4, 29: 19, 30: 28, 31: 43,
        32: 3, 33: 20, 34: 27, 35: 44,
        36: 2, 37: 21, 38: 26, 39: 45,
        40: 1, 41: 22, 42: 25, 43: 46,
        44: 0, 45: 23, 46: 24, 47: 47,
                       48: 49, 49: 48}


def startup_animation():
    for x in range(50):
        pixels[translate_pixel[x]] = (250,250,250)
        pixels.show()
        time.sleep(0.1)
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(0.5)

def show_frame(frame: Frame):
