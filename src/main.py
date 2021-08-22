from signal import signal, SIGINT
from sys import exit
import time
import RPi.GPIO as GPIO
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

#Handle exit
def handler(signal_received, frame):
    print("SIGINT or CTRL-C detected. Exiting.")
    #Draw black rectangle on screen
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    display.image(image)
    display.show()
    #Cleanup GPIO pins
    GPIO.cleanup(channel)
    exit(0)

if __name__ == '__main__':
    #Setup GPIO
    channel = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.IN)

    #Setup display
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

    signal(SIGINT, handler)

    #Main loop
    while True:

        val = GPIO.input(channel)

        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        if val == GPIO.LOW:
            draw.text((x, top + 0), "Lights: On", font=font, fill=255)
        else:
            draw.text((x, top + 0), "Lights: Off", font=font, fill=255)
        
        #Display image
        display.image(image)
        display.show()
        time.sleep(0.1)