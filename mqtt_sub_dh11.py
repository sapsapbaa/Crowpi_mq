#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import time
import RPi.GPIO as GPIO
import Adafruit_DHT
import paho.mqtt.publish as publish

# set type of the sensor
sensor = 11
# set pin number
pin = 4
button_pin = 26
# set board mode to GPIO.BOARD
GPIO.setmode(GPIO.BCM)
# setup button pin asBu input and buzzer pin as output
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#set script argruments
topic = sys.argv[1]
host = sys.argv[2]
if len(sys.argv)<=0:
    print("This script run with \n mqtt_sub_dh11 topic hostname")
else:
    try:
        while GPIO.input(button_pin) :
            # Try to grab a sensor reading.  Use the read_retry method which will retry up
            # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

            # Un-comment the line below to convert the temperature to Fahrenheit.
            # temperature = temperature * 9/5.0 + 32

            # Note that sometimes you won't get a reading and
            # the results will be null (because Linux can't
            # guarantee the timing of calls to read the sensor).
            # If this happens try again!
            if humidity is not None and temperature is not None:
                print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
                payload = str(temperature)+","+str(humidity)
                publish.single(topic, payload, hostname=host)
            else:
                print('Failed to get reading. Try again!')
            # Wait for 5 seconds
            time.sleep(5)
    except KeyboardInterrupt:
        GPIO.cleanup()
