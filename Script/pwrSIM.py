import serial
from time import sleep
import sys
from RPi_Driver import Send,ShutGSM

ser = serial.Serial('/dev/ttyAMA0',115200,timeout=10);

# Please Turn on the module and wait some seconds to use the module
# this module need some seconds to it works well. This process can 
# delay at least two minutes, please be patient. Use once to Turn ON
# the module and then use the other programms.

PWR = raw_input('Turn ON or OFF Module FONA808?'); # What do you do ? IN - OFF

if(PWR):
	# Initial command
	Send(ser,'AT\n','OK\r\n',1);
	# Delete Message of Module
	Send(ser,'AT+CMGD=1\n','OK\r\n',1);
	ShutGSM(ser);

	# Turn on the network of module
	ON_Net(ser,'AT+CGATT=1\n','OK\r\n',1);
	ON_Net(ser,'AT+CSTT="internet.comcel.com.co","comcel","comcel"\n','OK\r\n',1);
	ON_Net(ser,'AT+CIICR\n','OK\r\n',3);
	Send(ser,'AT+CIFSR\n','OK\r\n',1);

	# Active GPS
	Send(ser,'AT\n','OK\r\n',1);
	Send(ser,'AT+CGNSPWR=1\n','OK\r\n',1);
else:
	# Desactive GSM Antenna 
	Send(ser,'AT\n','OK\r\n',1);
	ShutGSM(ser);
	# Desactive GPS Antenna
	Send(ser,'AT\n','OK\r\n',1);
	Send(ser,'AT+CGNSPWR=0\n','OK\r\n',1);

def ON_Net(ser,str_TX,str_RX,line):
		Net = Send(ser,str_TX,str_RX,line);
		if(Net[0]=="E"):
			print "No hay conexion a internet";
			sys.exit(1);

