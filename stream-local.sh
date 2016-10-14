#!/bin/sh

raspivid --verbose --nopreview -hf --framerate 60 --bitrate 10000000 -vf --width 640 --height 480 --profile baseline --timeout 0 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! udpsink host=192.168.1.214 port=8004
