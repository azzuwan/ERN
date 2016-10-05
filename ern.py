#!/usr/bin/env python

import RPi.GPIO as GPIO, time, requests

street_light = 29
emergency_light = 31
ldr = 33
button = 37
pir = 35
press_count = 0
current_pir = 0
previous_pir =0
alert = True

GPIO.setmode(GPIO.BOARD)
GPIO.setup(street_light, GPIO.OUT)
GPIO.output(street_light, False)
GPIO.setup(emergency_light, GPIO.OUT)
GPIO.output(emergency_light, False)
GPIO.setup(pir, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

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

    if pir_value == 1 and previous_pir == 0 and ldr_value > 25000:
      print "Motion detected and it's dark"
      previous_pir = 1
      GPIO.output(street_light, True)
      time.sleep(10)
    elif pir_value == 1 and previous_pir == 0 and ldr_value < 25000:
      print "Motion detected but the sun is still out there"
      GPIO.output(street_light, False)
      time.sleep(0.1)
    else:
      print "No Motion"
      previous_pir = 0
      GPIO.output(street_light, False)
      time.sleep(0.1)


    current = GPIO.input(button)
    if (current == GPIO.LOW):
      print "PRESSED"
      GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
      #r = requests.get("http://192.168.0.3:9000/test")
      #print(r.text)
      GPIO.output(street_light, True)
    #   GPIO.output(emergency_light, True)
    #   time.sleep(15)
      while alert:
        GPIO.output(emergency_light, True)
        time.sleep(0.4)
        GPIO.output(emergency_light, False)
        time.sleep(0.4)
        if GPIO.input(button) == GPIO.LOW:
          GPIO.output(emergency_light, False)
          GPIO.output(street_light, False)
          break

      GPIO.output(emergency_light, False)
      GPIO.output(street_light, False)

except KeyboardInterrupt:
  pass
finally:
  GPIO.cleanup()
