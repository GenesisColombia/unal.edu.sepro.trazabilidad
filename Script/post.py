from time import sleep
import serial
from RPi_Driver import Send, ShutGSM, SendInfo
import requests

def send(Date,Lon,Lat,Alt,Temp,Hum):
	ser = serial.Serial('/dev/ttyAMA0',115200,timeout=1);
	payload = "{'token':123,'ruta':43,'temp':"+str(Temp)+",'hum':"+str(Hum)+",'fuerzag':0,'fecha':\""+str(Date)+"\",'lat':"+str(Lat)+",'lng':"+str(Lon)+"}"
	purl = 'POST /ords/sepro/tracking/ HTTP/1.0\nHost: ec2-54-174-66-58.compute-1.amazonaws.com:9090\nContent-Type: application/json\nContent-Length: '+str(len(payload))+'\n\n{"token":123,"ruta":43,"temp":'+str(Temp)+',"hum":'+str(Hum)+',"fuerzag":0,"fecha":"'+str(Date)+'","lat":'+str(Lat)+',"lng":'+str(Lon)+'}\n\x1A';
	send_return=Send(ser,'AT\n','OK\r\n',1);
	while not (send_return.find("ERROR")==-1):
		send_return=Send(ser,'AT\n','OK\r\n',1);
	send_return=Send(ser,'AT+CIPSTART="TCP","ec2-54-174-66-58.compute-1.amazonaws.com","9090"\n','CONNECT OK\r\n',4);
	print "Send_Return====>",send_return,"<========="
	print "Error--->",(send_return.find("ERROR")!=-1),"<------"
	print "Already--->",(send_return.find("ALREADY")!=-1),"<-----"
        while ((send_return.find("ERROR")!=-1) and (send_return.find("ALREADY")!=-1)):
		send_return=Send(ser,'AT+CIPCLOSE','CLOSE OK\r\n',1)
		print "Send_Return====",send_return
        	send_return=Send(ser,'AT+CIPSTART="TCP","ec2-54-174-66-58.compute-1.amazonaws.com","9090"\n','OK\r\nCONNECT OK\r\n',3);
        pwr=SendInfo(ser,purl);
	if (pwr=="pwr"):
		return pwr
	Send(ser,'AT+CIPCLOSE\n','',2)
