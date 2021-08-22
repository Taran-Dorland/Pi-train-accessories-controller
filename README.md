## Description

A controller to manage LED's and other automations for a model railroad easily in a web-browser using Python3 and Flask. Also includes an Adafruit PiOLED screen for immediate feedback.

## Requirements
### Hardware
- [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)
- [Adafruit PiOLED 128x32](https://www.adafruit.com/product/3527)

*Arduino(s) + other hardware to be listed later.

### Software
- [Adafruit PiOLED setup](https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/usage)

## Installation (In-dev)

*The Adafruit PiOLED setup **MUST** be completed on the Pi before the following.

1. Install required packages
`python -m pip install -r requirements.txt`
2. Setup flask environment
`export FLASK_APP=src/testflask`
`export FLASK_ENV=development`
3. - To access on local computer
   `flask run`
   - To access over local network
   `flask run --host=0.0.0.0`

## GPIO Pinout (RESERVED)
## Arduino code (RESERVED)
## Screenshots (RESERVED)