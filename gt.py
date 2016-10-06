#! /usr/bin/env python
# License: MIT
 
import os
from gps import *

gpsd = gps.gps(mode=WATCH_ENABLE)