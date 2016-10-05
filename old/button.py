#!/usr/bin/env python
import RPi.GPIO as GPIO, time, requests 
button = 15
red_led = 16
street_light = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(street_light, GPIO.OUT)
GPIO.output(street_light, False)
GPIO.setup(red_led, GPIO.OUT)
GPIO.output(red_led, False)

def button_pressed(channel):
	print("Button Pressed")

try:
	while True:
		if GPIO.input(button) == False:
			print("Button Pressed")
			r = requests.get("http://192.168.0.3:9000/test")			
			print(r.text)
			GPIO.output(red_led, True)
			GPIO.output(street_light, True)
			time.sleep(25)
			GPIO.output(red_led, False)
			GPIO.output(street_light, False)
			

except KeyboardInterrupt:
    pass
finally: GPIO.cleanup()



