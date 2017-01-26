import serial
from time import sleep
from RPi_Driver import Send,KeepGPS

ser = serial.Serial('/dev/ttyAMA0',115200,timeout=2);

Send(ser,'AT\n','OK\r\n',1);
Send(ser,'AT+CGNSSEQ="RMC"\n','OK\r\n',1);
# Keep information of GPS
KeepGPS(ser);

def write():
	return KeepGPS(ser);

