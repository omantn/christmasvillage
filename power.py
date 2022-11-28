import RPi.GPIO as GPIO 
import time

def switchPower(pin, state):
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin,GPIO.OUT)
	GPIO.output(pin,state)
