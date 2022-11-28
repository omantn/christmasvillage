import board
import neopixel
import time
import random


class lights:
    pixels = None
    numPixels = 0
    def __init__(self, pin, pixelcount, brightness):
        global pixels
        global numPixels
        pixels = neopixel.NeoPixel(pin, pixelcount, brightness=brightness, auto_write=False, pixel_order=neopixel.RGB)
        numPixels = pixelcount
        random.seed(1)

    def setPixelColor(self, pixel, color):
        global pixels
        pixels[pixel] = color
        pixels.show()

    def setNextColor(self, pixel, color):
        global pixels
        if color == 'fire':
            pixels[pixel] = (random.randint(25,90), random.randint(200,255), 0) 
            pixels.show()
        elif color == 'white':
            pixels[pixel] = (255, 255, 255)
            pixels.show()
        elif color == 'red':
            pixels[pixel] = (0, 255, 0)
            pixels.show()
        elif color == 'green':
            pixels[pixel] = (255, 0, 0)
            pixels.show()
        elif color == 'blue':
            pixels[pixel] = (0, 0, 255)
            pixels.show()
        elif color == 'yellow':
            pixels[pixel] = (255, 255, 0)
            pixels.show()
        elif color == 'aqua':
            pixels[pixel] = (142, 68, 173)
            pixels.show()
        elif color == 'purple':
            pixels[pixel] = (130, 0, 130)
            pixels.show()
        else:
            if color != pixels[pixel]:
               pixels[pixel] = color
               pixels.show()

    def allOff(self):
        global pixels
        global numPixels
        for i in range(numPixels):
            pixels[i] = (0, 0, 0)
        pixels.show()


