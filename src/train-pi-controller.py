import sys
from adafruit_framebuf import BitmapFont
from flask import Flask, render_template, request
from flask.wrappers import Request
import time
import RPi.GPIO as GPIO
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import atexit
import json

import getTrainInfo as TrainInfo

#----------------------------------------------------------------
# Handle application shutdown

def cleanExit():
    # Clear PiOLED display
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    display.image(image)
    display.show()
    # Cleanup RPi GPIO
    GPIO.cleanup()
    print("Clean exit.")

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

GPIO.setmode(GPIO.BCM)
GPIO.setup([ARD1_IN, ARD2_IN, ARD3_IN], GPIO.IN)
GPIO.setup([ARD1_OUT, ARD2_OUT, ARD3_OUT], GPIO.OUT)

# Handles turning lights on
def lightsOn():

    GPIO.output([ARD1_OUT, ARD2_OUT, ARD3_OUT], GPIO.HIGH)

    print("Lights toggle: ON", file=sys.stderr)
    updateDisplay("Toggle: ON")

# Handles turning lights off
def lightsOff():

    GPIO.output([ARD1_OUT, ARD2_OUT, ARD3_OUT], GPIO.LOW)

    print("Lights toggle: OFF", file=sys.stderr)
    updateDisplay("Toggle: OFF")


# 0 == Closed == Red; 1 == Thrown == Green
def rgbLight(val):
    GPIO.output(ARD1_OUT, val)

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
def updateDisplay(textToDisplay):
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((x, top + 0), textToDisplay, font=font, fill=255)
    display.image(image)
    display.show()
    time.sleep(0.1)

#----------------------------------------------------------------
# Logic

# Check if given turnout is thrown/closed
def checkTurnout(turnoutNum, turnoutData):
    val = turnoutData[turnoutNum]["data"]["state"]

    #2 == Closed turnout; 4 == Thrown turnout
    if val == 2:
        updateDisplay("Turnout[{0}]: Closed".format(turnoutNum))
        rgbLight(0)
    else:
        updateDisplay("Turnout[{0}]: Thrown".format(turnoutNum))
        rgbLight(1)


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
            checkTurnout(0, TrainInfo.getTurnouts())
    
    return render_template('index.html')

@app.route('/test')
def test():
    return "Test message."