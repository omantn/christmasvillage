import json
from traceback import print_tb
import board
import neopixel
import time
import random
import lighting
import power
import threading
import atexit
from gpiozero import LineSensor
from signal import pause
from flask import Flask, redirect, url_for, render_template, request
import RPi.GPIO as GPIO
import pwmio
import digitalio
lightson = True

def exit_handler():
    global powerPin
    houselights.allOff()
    power.switchPower(powerPin, False)

atexit.register(exit_handler)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/poweroff')
def poweroff():
    print('Power off requested.')
    powerOff()
    return redirect("/", code=302)

@app.route('/poweron')
def poweron():
    print('Power on requested.')
    powerOn()
    return redirect("/", code=302)

@app.route('/trainstop')
def trainstop():
    global A
    global B
    global analog_out
    A.value = False
    B.value = False
    print('Train stop requested.')
    analog_out.duty_cycle = 0
    return redirect("/", code=302)
@app.route('/trainstart')
def trainstart():
    global A
    global B
    global analog_out
    global trainhalfspeed
    A.value = True
    B.value = False
    print('Train start requested.')
    analog_out.duty_cycle = trainhalfspeed
    return redirect("/", code=302)
@app.route('/trainfull')
def trainfull():
    global A
    global B
    global analog_out
    global trainfullspeed
    A.value = True
    B.value = False
    print('Train full requested.')
    analog_out.duty_cycle = int(trainfullspeed / 4)
    time.sleep(3)
    analog_out.duty_cycle = int(trainfullspeed / 4) * 2
    time.sleep(3)
    analog_out.duty_cycle = int(trainfullspeed / 4) * 3
    time.sleep(3)
    analog_out.duty_cycle = trainfullspeed
    time.sleep(3)

    return redirect("/", code=302)
@app.route('/lightsoff')
def lightsoff():
    global lightson
    print('Lights off requested.')
    lightson=False
    return redirect("/", code=302)
@app.route('/lightson')
def lightsOn():
    global lightson
    print('Lights on requested.')
    lightson=True
    return redirect("/", code=302)
@app.route('/lights')
def lights():
    global village
    return render_template("lights.html", data = village)
@app.route('/setlight', methods=['POST'])
def setlight():
    global village
    print(request.form)
    village['houses'][int(request.form['neopixelid'])]['lightcolor'] = request.form['lightcolor']
    with open("christmasvillage.json", "w") as outfile:
    	outfile.write(json.dumps(village,indent = 4))
    return redirect("/lights", code=302)

def doLights():
    global lightson
    global village
    global houselights
    try:
        while True:
            for i in village['houses']:
                if lightson == True:
                    houselights.setNextColor(i['neopixelid'],i['lightcolor'])
                else:
                    houselights.allOff()
            time.sleep(0.2)
    except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt
        exit_handler

def trainInstructionPut(instruction):
    try:
        global trainstartpin
        global trainstoppin
        global trainfullpin
        
        if instruction == 0:
            pinToSend = trainstartpin
        elif instruction == 1:
            pinToSend = trainstoppin
        elif instruction == 2:
            pinToSend = trainfullpin
        print("Sending " + str(pinToSend) + " to train")
        GPIO.output(pinToSend, 1)
        time.sleep(0.2)
        GPIO.output(pinToSend, 0)

    except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt
        exit_handler

def powerOff():
    global powerPin
    print(powerPin)
    power.switchPower(powerPin, False)

def powerOn():
    global powerPin
    power.switchPower(powerPin, True)

def proxDetected(proxpin):
    print("Train over prox sensor " + str(proxpin))

# Main program begins here
print('Christmas Village version 0.1')

print('Loading configuration...')
f=open('christmasvillage.json')
village = json.load(f)

for i in village['houses']:
    print(i['name'] + ': ' + i['lightcolor'])

f.close()

pin = getattr(board, f"D{village['neopixelpin']}")
pixelCount=len(village['houses'])
print('houses configured.........' + str(pixelCount))
powerPin=village['power']
print('power switch pin..........' + str(powerPin))

print('Initializing lights...')
houselights = lighting.lights(pin,pixelCount,village['brightness'])

print('Starting light thread...')
lightthread = threading.Thread(target=doLights)
lightthread.start()

print('Starting prox checking...')
sensor1 = LineSensor(village['prox1'])
sensor1.when_line = lambda: proxDetected(1)
sensor2 = LineSensor(village['prox2'])
sensor2.when_line = lambda: proxDetected(2)
sensor3 = LineSensor(village['prox3'])
sensor3.when_line = lambda: proxDetected(3)
sensor4 = LineSensor(village['prox4'])
sensor4.when_line = lambda: proxDetected(4)

print('Initializing train power...')
analog_out = pwmio.PWMOut(getattr(board, f"D{village['trainoutpin']}"),duty_cycle=0)
A = digitalio.DigitalInOut(getattr(board, f"D{village['trainapin']}"))
A.direction = digitalio.Direction.OUTPUT
B = digitalio.DigitalInOut(getattr(board, f"D{village['trainbpin']}"))
B.direction = digitalio.Direction.OUTPUT
A.value = True
B.value = False
trainhalfspeed = village['trainhalfspeed']
trainfullspeed = village['trainfullspeed']

print('Starting web server...')
try:
	app.run(host='0.0.0.0',port=80)

except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt
        lightthread.terminate()
        exit_handler

