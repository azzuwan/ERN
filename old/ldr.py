#!/usr/bin/env python

import RPi.GPIO as GPIO, time

ldr = 7
street_light = 11
pir = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(street_light, GPIO.OUT)
GPIO.setup(pir, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)



def RCTime(pin):
  count = 0

  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, GPIO.LOW)
  time.sleep(0.1)

  GPIO.setup(pin, GPIO.IN)

  while(GPIO.input(pin) == GPIO.LOW):
    count += 1

  return count

try:
  while True:
    pir_value = GPIO.input(pir)
    ldr_value = RCTime(ldr)
    print ldr_value    
      
    if pir_value == 1 and ldr_value > 12000:
      print "Motion detected and it's dark"
      GPIO.output(street_light, True)
      time.sleep(0.1)
    elif pir_value == 1 and ldr_value < 12000:
      print "Motion detected but the sun is still out there"
      GPIO.output(street_light, False)
      time.sleep(0.1)
    else:
      print "No Motion"
      GPIO.output(street_light, False)
      time.sleep(0.1)
      
except KeyboardInterrupt:
  pass
finally:
  GPIO.cleanup()
