import serial
from time import sleep
from RPi_Driver import Send,KeepGPS

ser = serial.Serial('/dev/ttyAMA0',115200,timeout=2);

Send(ser,'AT\n','OK\r\n',1);
Send(ser,'AT+CGNSPWR=1\n','OK\r\n',1);
sleep(1);
Send(ser,'AT+CGNSSEQ="RMC"\n','OK\r\n',1);
# Keep information of GPS
Date,Lon,Lat = KeepGPS(ser);
Send(ser,'AT+CGNSPWR=0\n','OK\r\n',1);
print Date;
print Lon;
print Lat;
