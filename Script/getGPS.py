import serial 
from time import sleep

ser = serial.Serial('/dev/ttyAMA0',115200);
ser.write(b'AT\r\n');
sleep(2);
ser.write(b'AT+CMGF=1\r\n');
sleep(2);
ser.write(b'AT+CMGS="+573128464383"\r\n');
sleep(2);
ser.write(b"Como Erika dijo, eventualmente lo consegui, este es tu premio. Te quiero Att: Modulo de Jairo :)\r\n");
ser.write(b'\x1A');
sleep(2);
