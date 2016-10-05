#!/usr/bin/env python

import RPi.GPIO as GPIO, time

GPIO.setmode(GPIO.BOARD)
pin = 13
light = 11
GPIO.setup(pin, GPIO.OUT)
GPIO.setup(light, GPIO.OUT)
GPIO.output(pin, GPIO.LOW)
time.sleep(0.5)

def RCtime (p):
  measurement = 0
  # Discharge capacitor
  GPIO.setup(p, GPIO.OUT)
  GPIO.output(p, GPIO.LOW)
  time.sleep(0.1)

  GPIO.setup(p, GPIO.IN)
  # Count loops until voltage across
  # capacitor reads high on GPIO
  while (GPIO.input(p) == GPIO.LOW):
    measurement += 1

  return measurement


try:
  while True:
    value = RCtime(pin)
    print value
    if(value > 25000):
        GPIO.output(light, GPIO.HIGH)
        time.sleep(10)
        GPIO.output(light, GPIO.LOW)

except KeyboardInterrupt:
  pass
finally:
  GPIO.cleanup()
