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

#----------------------------------------------------------------
# Handle RPi.GPIO



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

# Turn on lights
def turnOn():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((x, top + 0), "Toggle: ON", font=font, fill=255)
    display.image(image)
    display.show()
    time.sleep(0.1)

# Turn off lights
def turnOff():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((x, top + 0), "Toggle: OFF", font=font, fill=255)
    display.image(image)
    display.show()
    time.sleep(0.1)

#----------------------------------------------------------------
# Flask app

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():

    if request.method == 'POST':
        if request.form['submit_button'] == '0':
            print("Turn on.", file=sys.stderr)
            turnOn()
        elif request.form['submit_button'] == '1':
            print("Turn off.", file=sys.stderr)
            turnOff()
    
    return render_template('index.html')

@app.route('/test')
def test():
    return "Test message."