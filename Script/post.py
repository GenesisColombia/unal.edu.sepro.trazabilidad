from time import sleep
import serial
from RPi_Driver import Send, ShutGSM, SendInfo

ser = serial.Serial('/dev/ttyAMA0',115200,timeout=5);
purl = 'POST /api/v1.6/variables/581ded2476254279db1c61d5/values HTTP/1.1\nX-Auth-Token: rOfsYDEkAPCN5osWWpOiwOf1R7Lnd2\nHost: things.ubidots.com\nConnection: close\nContent-Type: application/json\nContent-Length: 60\n\n{"value":10, "context":{"lat": 4.628008, "lng":-74.090494}}\n\x1A';

Send(ser,'AT\n','OK\r\n',1);
Send(ser,'AT+CIPSTART="TCP","things.ubidots.com","80"\n','CONNECT OK\r\n',3);
SendInfo(ser,purl);
ShutGSM(ser);
