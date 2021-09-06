from asyncio.events import get_event_loop
import sys
from adafruit_framebuf import BitmapFont
from flask import Flask, render_template, request
import time
import RPi.GPIO as GPIO
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import atexit, threading
import json

import getTrainInfo as TrainInfo

#
# Important
KILL_THREADS = 0

#----------------------------------------------------------------
# Handle application shutdown

def cleanExit():
    # Clear PiOLED display
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    display.image(image)
    display.show()
    # Cleanup RPi GPIO
    GPIO.cleanup()
    global KILL_THREADS
    KILL_THREADS = 1
    print("Clean exit.")
    time.sleep(1)

#----------------------------------------------------------------
# GPIO Layout: https://pinout.xyz/
# Handle RPi.GPIO

# Each of these board pinouts maps to an Arduino Nano that will
# toggle the LEDs controlled by that Arduino
ARD1_IN = 14
ARD2_IN = 15
ARD3_IN = 18

ARD1_OUT = 17
ARD2_OUT = 27
ARD3_OUT = 22
ARD4_OUT = 10

ARD_OUTS = [ARD1_OUT, ARD2_OUT, ARD3_OUT, ARD4_OUT]

GPIO.setmode(GPIO.BCM)
GPIO.setup([ARD1_IN, ARD2_IN, ARD3_IN], GPIO.IN)
GPIO.setup([ARD1_OUT, ARD2_OUT, ARD3_OUT, ARD4_OUT], GPIO.OUT)

# Handles turning lights on
def lightsOn():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    GPIO.output(ARD_OUTS, GPIO.HIGH)
    print("Lights toggle: ON", file=sys.stderr)
    updateDisplay("Toggle: ON")

# Handles turning lights off
def lightsOff():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    GPIO.output(ARD_OUTS, GPIO.LOW)
    print("Lights toggle: OFF", file=sys.stderr)
    updateDisplay("Toggle: OFF")


# 0 == Closed == Red; 1 == Thrown == Green
def rgbLightToggle(pin, val):
    GPIO.output(pin, val)

#----------------------------------------------------------------
# Handle PiOLED

# Setup display
i2c = busio.I2C(SCL, SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
display.fill(0)
display.show()

width = display.width
height = display.height
image = Image.new("1", (width, height))

draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=0)

padding = -2
top = padding
bottom = height - padding
x = 0

font = ImageFont.load_default()

# Setup atexit
atexit.register(cleanExit)

# Update screen
def updateDisplay(textToDisplay, topAdd=0):
    #draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((x, top + topAdd), textToDisplay, font=font, fill=255)
    display.image(image)
    display.show()
    time.sleep(0.1)

#----------------------------------------------------------------
# Logic

# Check if given turnout is thrown/closed
def checkTurnout(turnoutNum, turnoutData, pinout, screenTop=0):
    val = turnoutData["data"]["state"]

    #2 == Closed turnout; 4 == Thrown turnout
    if val == 2:
        updateDisplay("Turnout[{0}]: Closed".format(turnoutNum), screenTop)
        rgbLightToggle(pinout, 0)
    else:
        updateDisplay("Turnout[{0}]: Thrown".format(turnoutNum), screenTop)
        rgbLightToggle(pinout, 1)

#----------------------------------------------------------------
# Threading

def updateTurnouts():
    while True:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        turnoutData = TrainInfo.getTurnouts()

        for i in range(4):
            checkTurnout(i, turnoutData[i], ARD_OUTS[i], i*8)

        if KILL_THREADS == 1:
            print("Time to end thread.")
            break
        else:
            time.sleep(3)
    
listenThread = threading.Thread(target=updateTurnouts)
#----------------------------------------------------------------
# Flask app

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():

    if request.method == 'POST':
        if request.form['submit_button'] == '0':
            print("Turn on.", file=sys.stderr)
            lightsOn()
        elif request.form['submit_button'] == '1':
            print("Turn off.", file=sys.stderr)
            lightsOff()
        elif request.form['submit_button'] == '2':
            try:
                listenThread.start()
            except:
                print("Failed to start thread.")
    
    return render_template('index.html')

@app.route('/test')
def test():
    return "Test message."