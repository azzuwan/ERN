#!/usr/bin/env python

import RPi.GPIO as GPIO, datetime, picamera

camera = picamera.PiCamera()

camera.capture( str(datetime.datetime.now()) + ".jpg");
