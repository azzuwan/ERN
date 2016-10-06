#! /usr/bin/env python
# License: MIT
 
import os, time
from gps import *


gpsd = gps(mode=WATCH_ENABLE)

for x in range(0, 30):
  gpsd.next()
  print gpsd.fix.latitude, ", ", gpsd.fix.longitude
  time.sleep(1.5)