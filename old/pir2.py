#!/usr/bin/env python
import RPi.GPIO as GPIO, time

GPIO.setmode(GPIO.BOARD)

for i in range(1,40):
    if (i != 1 and i != 2 and i != 17 and i != 3 and i != 5 and i != 4 and i != 6 and i != 9 and i != 14 and i != 20 and i != 28 and i != 30 and i != 34 and i != 39 and i != 27 and i != 25):
        print "Current Pin: ", i
        GPIO.setup(i, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

for i in range(1,40):
    if (i != 1 and i != 2 and i != 17 and i != 3 and i != 5 and i != 4 and i != 6 and i != 9 and i != 14 and i != 20 and i != 28 and i != 30 and i != 34 and i != 39 and i != 27 and i != 25):
        input = GPIO.input(i)
        print "Current INPUT PIN: ", i, "VALUE: ", input
