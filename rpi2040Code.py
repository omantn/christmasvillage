import time
import board
import digitalio
import pwmio

#pin = getattr(board, f"D{7}")
analog_out = pwmio.PWMOut(board.GP7,duty_cycle=0)

stop = digitalio.DigitalInOut(board.GP18)
stop.direction = digitalio.Direction.INPUT
stop.pull = digitalio.Pull.DOWN

start = digitalio.DigitalInOut(board.GP19)
start.direction = digitalio.Direction.INPUT
start.pull = digitalio.Pull.DOWN

full = digitalio.DigitalInOut(board.GP22)
full.direction = digitalio.Direction.INPUT
full.pull = digitalio.Pull.DOWN


A = digitalio.DigitalInOut(board.GP8)
A.direction = digitalio.Direction.OUTPUT

B = digitalio.DigitalInOut(board.GP9)
B.direction = digitalio.Direction.OUTPUT

print("startup")

while True:
    if stop.value:
        print("I see a value on stop!")
        analog_out.duty_cycle = 0
        time.sleep(0.5)
    if start.value:
        print("I see a value on start!")
        analog_out.duty_cycle = 8000
        time.sleep(0.5)
    if full.value:
        print("I see a value on full!")
        analog_out.duty_cycle = 12000
        time.sleep(0.5)
    A.value = True
    B.value = False


