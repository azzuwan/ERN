#!/usr/bin/env python

import RPi.GPIO as GPIO, time

GPIO.setmode(GPIO.BOARD)
pin = 35
#GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN, initial=0)
GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
input = GPIO.input(pin)
print "INITIAL INPUT STATE IS ", input
current = 0
previous = 0


try:
  while True:
    current  = GPIO.input(pin)
    if current == 1 and previous == 0:
        print "MOTION DETECTED ", current
        previous = 1
    elif current == 0 and previous ==1:
        print "NO MOTION "
        previous = 0

except KeyboardInterrupt:
  pass
finally:
  GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
  GPIO.cleanup()
