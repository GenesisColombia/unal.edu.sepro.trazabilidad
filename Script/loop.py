#!/usr/bin/python
import time
import getGPS
import getTempHum
import post
import datetime

while (1):
	
	Date,Lon,Lat,Alt =getGPS.write()
	Date=datetime.datetime.strptime(str(int(float(Date))),'%Y%m%d%H%M%S')
	print "Date,Lon,Lat,Alt",Date,Lon,Lat,Alt
	Temp=0
	Hum=0
	print "reset...",Temp,Hum
	Hum,Temp=getTempHum.write()
	post.send(Date,Lon,Lat,Alt,Temp,Hum)
	print "TemperaHumedad...",Temp,Hum
	time.sleep(3)
