#!/usr/bin/env python
import RPi.GPIO as GPIO, time
 
red_led = 16
button = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(button, GPIO.IN)
GPIO.setup(red_led, GPIO.OUT)
print "LED On"

try:

	GPIO.output(red_led, True)
	time.sleep(20)
	GPIO.output(red_led, False)
except KeyboardInterrupt:
    pass
finally: GPIO.cleanup()
        
