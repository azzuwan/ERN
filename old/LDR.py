#!/usr/bin/env python

import RPi.GPIO as GPIO, time, os



DEBUG = 1
GPIO.setmode(GPIO.BCM)

RED = 17
GREEN = 11
PIN = 13
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)

def RCtime(RCpin):
  reading = 0
  GPIO.setup(RCpin, GPIO.OUT)
  GPIO.output(RCpin, GPIO.LOW)
  time.sleep(0.1)
  GPIO.setup(RCpin, GPIO.IN)
  while (GPIO.input(RCpin) == GPIO.LOW):
    reading += 1
  return reading

while True:
  print RCtime(PIN)
  if RCtime(PIN) > 1000:
    GPIO.output(RED, True)
    GPIO.output(GREEN, False)
  elif RCtime(PIN) < 1000:
    GPIO.output(RED, False)
    GPIO.output(GREEN, True)
  else:
    GPIO.output(RED, False)
    GPIO.output(GREEN, False)


GPIO.cleanup()
