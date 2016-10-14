#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import os
import requests
import threading
import rethinkdb as rdb
from gps import *

#This ERN node id
node_id = os.environ["NODE_ID"]

#The ERN server ip address or domain name
ern_server = "192.168.1.214"

#The RethinkDB client port
ern_port = 28015

#The RethinkDB database
ern_db = "ERN"

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
alert = False

#Flag to allow threads to exit
stop_threads = False

t_distress = None

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
  while not stop_threads:    
    #Get motion detector value
    pir_value = GPIO.input(pir)
    
    #Get light sensor value
    ldr_value = RCTime(ldr)
    #print ldr_value

    #If motion is detected and it's low light turn on the street light
    #for 10 seconds
    if pir_value == 1 and previous_pir == 0 and ldr_value > 25000:
      #print "Motion detected and it's dark"
      previous_pir = 1
      GPIO.output(street_light, True)
      time.sleep(10)      
    #If motion is detected but it is still bright, make sure the lights 
    #are off
    elif pir_value == 1 and previous_pir == 0 and ldr_value < 25000:
      #print "Motion detected but the sun is still out there"
      GPIO.output(street_light, False)
      time.sleep(0.1)    
    else:
      print "No Motion"
      previous_pir = 0
      GPIO.output(street_light, False)
      time.sleep(0.1)

def signal_alert():
  global alert
  while alert:    
    GPIO.output(emergency_light, True)
    time.sleep(0.4)
    GPIO.output(emergency_light, False)
    time.sleep(0.4)

def update_status():
  print "STATUS UPDATE:"
  while not stop_threads:
    global lat, lng
    rdb.connect(host=ern_server, port=ern_port, db=ern_db).repl()
    cursor = rdb.table("nodes").filter(lambda node: node["node_id"].match(node_id)).run()
    nodes = list(cursor)
    timestamp = time.time()
    if nodes:
      node = nodes[0]
      print "Updating node: ", node_id, ", @ ", str(lat), ", " ,str(lng), " ", timestamp, " status = online" 
      rdb.table("nodes").get(node["id"]).update({ "lat" : str(lat), "lng" : str(lng), "timestamp" : timestamp , "status": "online"}).run()
    else:
      print "Registering new node: ", node_id, ", @ ", str(lat), ", " ,str(lng)
      rdb.table("nodes").insert({"node_id" : str(node_id), "lat" : str(lat), "lng" : str(lng), "timestamp" : timestamp , "status": "online" }).run()      
    time.sleep(5)

def send_offline_status():
  global conn, rdb, lat, lng
  rdb.connect(host=ern_server, port=ern_port, db=ern_db).repl()  
  cursor = rdb.table("nodes").filter(lambda node: node["node_id"].match(node_id)).run()
  nodes = list(cursor)
  timestamp = time.time()
  print "Offline Mode: ", node_id, ", @ ", str(lat), ", " ,str(lng), " ", timestamp, " status = offline" 
  if nodes:
    node = nodes[0]      
    rdb.table("nodes").get(node["id"]).update({ "lat" : str(lat), "lng" : str(lng), "timestamp" : timestamp , "status": "offline"}).run()
  else:      
    rdb.table("nodes").insert({"node_id" : str(node_id), "lat" : str(lat), "lng" : str(lng), "timestamp" : timestamp ,"status": "offline" }).run()      

def send_distress_signal(alert_type):
  print "Sending distress signal to ERN server!!!"
  timestamp = time.time()
  rdb.connect(host=ern_server, port=ern_port, db=ern_db).repl()
  rdb.table("alerts").insert({"node_id" : str(node_id), "lat": str(lat), "lng": str(lng), "timestamp" : timestamp, "alert_type": alert_type}).run()

def button_pressed(channel):     
  global alert, t_distress
  print "EMERGENCY BUTTON PRESSED!"
  print "CURRENT ALERT STATUS: ", alert
  
  
  if alert == False:    
    alert = True    
    GPIO.output(street_light, True)
    t_alert = threading.Thread(target = signal_alert)
    t_alert.start()    
    t_distress = threading.Thread(target = send_distress_signal, args=["button"])
    t_distress.start()
    t_distress.join()   
  else:    
    alert = False    
    GPIO.output(emergency_light, False)
    GPIO.output(street_light, False)

#Manage GPS
def check_location():
  while not stop_threads:
    global lat,lng    
    gpsd.next()
    lat = gpsd.fix.latitude
    lng = gpsd.fix.longitude
    #print "Latitude: ", lat, ", Longitude: ", lng
    time.sleep(2)

try:
  GPIO.add_event_detect(button, GPIO.FALLING, callback=button_pressed, bouncetime=300)

  t_location = threading.Thread(target = check_location)
  t_light    = threading.Thread(target = check_light)
  t_status   = threading.Thread(target = update_status)  

  t_location.start()
  t_light.start()
  t_status.start()  
  
  while True:
    time.sleep(10)
    pass

except KeyboardInterrupt:
  print""
  print "Stopping ERN..."
  stop_threads = True
  t_location.join()
  t_light.join()
  t_status.join()
  send_offline_status()
  if not t_distress:
    t_distress.join()
  pass
finally:
  print "Goodbye!" 
  GPIO.cleanup()