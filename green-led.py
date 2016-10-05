#!/usr/bin/env python

import RPi.GPIO as GPIO, time, requests

green =  29

GPIO.setmode(GPIO.BOARD)
GPIO.setup(green, GPIO.OUT)
GPIO.output(green, False)

time.sleep(0.1)
GPIO.output(green, True)
time.sleep(3)
GPIO.output(green, False)
time.sleep(3)
GPIO.output(green, True)
time.sleep(3)
GPIO.output(green, False)
