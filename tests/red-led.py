#!/usr/bin/env python

import RPi.GPIO as GPIO, time, requests

red =  31

GPIO.setmode(GPIO.BOARD)
GPIO.setup(red, GPIO.OUT)
GPIO.output(red, False)

time.sleep(0.1)
GPIO.output(red, True)
time.sleep(3)
GPIO.output(red, False)
time.sleep(3)
GPIO.output(red, True)
time.sleep(3)
GPIO.output(red, False)
