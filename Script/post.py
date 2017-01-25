from time import sleep
import serial
from RPi_Driver import Send, ShutGSM, SendInfo

def send(Date,Lon,Lat,Alt,Temp,Hum):
	ser = serial.Serial('/dev/ttyAMA0',115200,timeout=5);

	purl = 'POST /ords/sepro/tracking/ HTTP/1.1\nHost: ec2-54-174-66-58.compute-1.amazonaws.com:9090\nContent-Type: application/json\nContent-Length: 60\n\n{"token":123,"ruta":43,"temp":'+str(Temp)+',"hum":'+str(Hum)+',"fuerzag":0,"fecha":"'+str(Date)+'","lat":'+str(Lat)+',"lng":'+str(Lon)+'}\n\x1A';
	Send(ser,'AT\n','OK\r\n',1);
        Send(ser,'AT+CIPSTART="TCP","ec2-54-174-66-58.compute-1.amazonaws.com","9090"\n','CONNECT OK\r\n',3);
        SendInfo(ser,purl);

