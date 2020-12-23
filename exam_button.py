#!/usr/bin/python

import sys
import time
import Adafruit_DHT
import json
import httplib, urllib
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.IN)
GPIO.setup(17,GPIO.OUT)

deviceId = "DyEQAWiP"

deviceKey = "f2L2cCGEmI8zrpAA"

sw=1
def post_to_mcs(payload): 
	headers = {"Content-type": "application/json", "deviceKey": deviceKey} 
	not_connected = 1 
	while (not_connected):
		try:
			conn = httplib.HTTPConnection("api.mediatek.com:80")
			conn.connect() 
			not_connected = 0 
		except (httplib.HTTPException, socket.error) as ex: 
			print("Error: %s" % ex) 
			time.sleep(1)
 
	conn.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload), headers) 
	response = conn.getresponse() 
	print( response.status, response.reason, json.dumps(payload), time.strftime("%c")) 
	data = response.read() 
	conn.close()

#sensor_args = { '11': Adafruit_DHT.DHT11,
#                '22': Adafruit_DHT.DHT22,
#                '2302': Adafruit_DHT.AM2302 }
#if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
#    sensor = sensor_args[sys.argv[1]]
#    pin = sys.argv[2]
#else:
#    print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
#    print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
#    sys.exit(1)

while 1:
       	sw = GPIO.input(22)
       	if sw==1:	
	       	GPIO.output(17,0)
                sw = 0
                print('turn off the switch')
	else:
		GPIO.output(17,1)
                sw = 1
	       	print('turn on the switch')
        
	payload = {"datapoints":[{"dataChnId":"dataswitch","values":{"value":sw}}]}


        post_to_mcs(payload)			
