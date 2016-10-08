#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import requests
import threading
from gps import *

#The normal street light
street_light = 29

#Emergency strobe light or can be just any type of light
emergency_light = 31

#Light sensor
ldr = 33

#Emergency Button
button = 37

#Motion detector
pir = 35

#GPSD client
gpsd = gps(mode=WATCH_ENABLE)

lat = None
lng = None

#Keep tracks of emergency button presses
press_count = 0

#Keeping track of pir values
current_pir = 0
previous_pir =0

#Toggles emergency status
alert = True

#Board setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(street_light, GPIO.OUT)
GPIO.output(street_light, False)
GPIO.setup(emergency_light, GPIO.OUT)
GPIO.output(emergency_light, False)
GPIO.setup(pir, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

#Manage light sensor
def RCTime(pin):
  global GPIO
  #Low pulse counter
  count = 0
  #Clear the previous pin state
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, GPIO.LOW)
  time.sleep(0.1)
  #Reset pin as input again
  GPIO.setup(pin, GPIO.IN)
  #Start counting low pulse from light sensor
  while(GPIO.input(pin) == GPIO.LOW):
    count += 1
  return count

#Manage street light
def check_light():
  global GPIO, previous_pir, pir_value, ldr_value 
  while True:    
    #Get motion detector value
    pir_value = GPIO.input(pir)
    
    #Get light sensor value
    ldr_value = RCTime(ldr)
    print ldr_value

    #If motion is detected and it's low light turn on the street light
    #for 10 seconds
    if pir_value == 1 and previous_pir == 0 and ldr_value > 25000:
      print "Motion detected and it's dark"
      previous_pir = 1
      GPIO.output(street_light, True)
      time.sleep(10)      
    #If motion is detected but it is still bright, make sure the lights 
    #are off
    elif pir_value == 1 and previous_pir == 0 and ldr_value < 25000:
      print "Motion detected but the sun is still out there"
      GPIO.output(street_light, False)
      time.sleep(0.1)    
    else:
      print "No Motion"
      previous_pir = 0
      GPIO.output(street_light, False)
      time.sleep(0.1)

def check_button():
  global GPIO
  #If the emergency button i spressed
  current = GPIO.input(button)
  while True:
    if (current == GPIO.LOW):
      print "EMERGENCY BUTTON PRESSED!"
      #Reset the button
      GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
      #r = requests.get("http://192.168.0.3:9000/test")
      #print(r.text)
      #Turn on the street light
      GPIO.output(street_light, True)
      #   GPIO.output(emergency_light, True)
      #   time.sleep(15)

      while alert:
        GPIO.output(emergency_light, True)
        time.sleep(0.4)
        GPIO.output(emergency_light, False)
        time.sleep(0.4)
        #If the emergency button is pressed the second time
        #turn the lights off
        if GPIO.input(button) == GPIO.LOW:
          GPIO.output(emergency_light, False)
          GPIO.output(street_light, False)
          break

      #Once the emergency loop is over switch off the lights      
      GPIO.output(emergency_light, False)
      GPIO.output(street_light, False)

#Manage GPS
def check_location():
  while True:
    global lat,lng
    #Get GPS location
    gpsd.next()
    lat = gpsd.fix.latitude
    lng = gpsd.fix.longitude
    print "Latitude: ", lat, ", Longitude: ", lng
    time.sleep(0.1)


try:
  #Main program loop
  t_location = threading.Thread(target = check_location)
  t_light    = threading.Thread(target = check_light)
  t_button   = threading.Thread(target = check_button)

  t_location.start()
  t_light.start()
  t_button.start()
  #check_location();
  #check_light();
  #check_button();
  while True:
    time.sleep(0.1)
    pass

except KeyboardInterrupt:
  pass
finally:
  GPIO.cleanup()