#!/usr/bin/env python
import RPi.GPIO as GPIO, time, requests

street_light = 29
emergency_light = 31
button = 37
alert = True

GPIO.setmode(GPIO.BOARD)
GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(street_light, GPIO.OUT)
GPIO.setup(emergency_light, GPIO.OUT)

def alert(channel):
   if alert:
     while alert:
        GPIO.output(emergency_light, True)
        time.sleep(0.4)
        GPIO.output(emergency_light, False)
        time.sleep(0.4)
        if GPIO.input(button) == GPIO.LOW:
          GPIO.output(emergency_light, False)
          GPIO.output(street_light, False)
        break

GPIO.add_event_detect(button, GPIO.FALLING, callback=alert, bouncetime=300)

try:
  while True:
     #GPIO.wait_for_edge(butti)
     print ""
     time.sleep(60)
except KeyboardInterrupt:
  pass
finally:
  GPIO.cleanup()
