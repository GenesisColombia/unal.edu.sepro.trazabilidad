#!/usr/bin/python
import time
import pwrSIM
import getGPS
import getTempHum
import post
import datetime

#pwrSIM.pwr_OFF()
pwrSIM.pwr_ON()
while (1):
	GPS=getGPS.write()
	while (len(GPS)<4):
		print "GPS Len:",len(GPS)
		GPS=getGPS.write()
	print "GPS Len:",len(GPS)
	Date,Lat,Lon,Alt =GPS
	Date=datetime.datetime.strptime(str(int(float(Date))),'%Y%m%d%H%M%S')
	Hum,Temp=getTempHum.write()
	Hum='%.4f'%(Hum)
	Temp= '%.4f'%(Temp)
	pwr=post.send(Date,Lon,Lat,Alt,Temp,Hum)
	if (pwr=="pwr"):
		pwrSIM.pwr_ON()
	time.sleep(2)
