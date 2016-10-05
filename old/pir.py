#!/usr/bin/env python

import RPi.GPIO as GPIO, time

GPIO.setmode(GPIO.BOARD)
pin = 40
#GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN, initial=0)
GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
input = GPIO.input(pin)
print "INITIAL INPUT STATE IS ", input
try:
  while True:
    input = GPIO.input(pin)
    if input == 0:
        print "Nothing moves"
        time.sleep(0.1)
    else:
        print "Motion detected!"
        time.sleep(0.1)

except KeyboardInterrupt:
  pass
finally:
  GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
  GPIO.cleanup()
