#!/bin/sh

curl -s 'http://localhost:8080/janus?gateway_url=http://192.168.1.214:8088&gateway_root=/janus&room=1234&room_pin=&username=test&proxy_host=&proxy_port=80&proxy_password=&proxy_bypass=&token=&publish=1&subscribe=0&hw_vcodec=0&vformat=60&reconnect=1&action=Start' > /dev/null
