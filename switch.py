#!/usr/bin/env python

import RPi.GPIO as GPIO, time

GPIO.setmode(GPIO.BOARD)
pin = 37
GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


try:
  while True:
    current = GPIO.input(pin)
    if (current == GPIO.LOW):
        print "PRESSED"
        GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        time.sleep(0.5)

except KeyboardInterrupt:
  pass
finally:
  GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
  GPIO.cleanup()
