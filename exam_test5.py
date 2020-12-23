#!/usr/bin/python

import sys
import time
import Adafruit_DHT
import json
import httplib, urllib
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.IN)

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

while 1:
       	sw = GPIO.input(22)
       	if sw==1:	
	       	sw = 0
                print('turn off the switch')
	else:
		sw = 1
	       	print('turn on the switch')
        
	payload = {"datapoints":[{"dataChnId":"dataswitch","values":{"value":sw}}]}


        post_to_mcs(payload)
