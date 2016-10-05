#!/usr/bin/env python

import RPi.GPIO as GPIO, time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.IN)
try:
  while True:
    reading = 0
    
    print "LOW"
    time.sleep(1)

except KeyboardInterrupt:
  pass
finally:
  GPIO.cleanup()
