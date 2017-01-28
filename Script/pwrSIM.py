import serial
from time import sleep
import sys
from RPi_Driver import Send,ShutGSM

# Please Turn on the module and wait some seconds to use the module
# this module need some seconds to it works well. This process can 
# delay at least two minutes, please be patient. Use once to Turn ON
# the module and then use the other programms.

def Net_Mistake(ser,str_TX,str_RX,line):
	Net = Send(ser,str_TX,str_RX,line);
	if(Net.find("ERROR")!=-1):
		print "No hay conexion a internet";
		return 0;

def Net_ON();
	# Turn on the network of module
	ShutGSM(ser);
	Net_Mistake(ser,'AT+CGATT=1\n','OK\r\n',1);
	Net_Mistake(ser,'AT+CSTT="internet.movistar.com.co","movistar","movistar"\n','OK\r\n',1);
	net=Net_Mistake(ser,'AT+CIICR\n','OK\r\n',3);
	if (net==0):
		pwr_ON();
		return 0;
	Send(ser,'AT+CIFSR\n','OK\r\n',1);

	# Active GPS
	Send(ser,'AT\n','OK\r\n',1);
	Send(ser,'AT+CGNSPWR=1\n','OK\r\n',1);

def pwr_OFF():
	# Desactive GSM Antenna 
	Send(ser,'AT\n','OK\r\n',1);
	ShutGSM(ser);
	# Desactive GPS Antenna
	Send(ser,'AT\n','OK\r\n',1);
	Send(ser,'AT+CGNSPWR=0\n','OK\r\n',1);

def pwr_ON():
	# Initial command
	ser = serial.Serial('/dev/ttyAMA0',115200,timeout=2);
	ok=Send(ser,'AT\n','OK\r\n',1);
	if (ok.find("ERROR")!=-1):
		ok=Send(ser,'AT\n','OK\r\n',1);
		if (ok.find("ERROR")!=-1):
			reset_FONA()
			return 0
	# Delete Message of Module
	Send(ser,'AT+CMGD=1\n','OK\r\n',1);


def reset_FONA():
	#pin(8).low
	#sleep(1)
	print "Hard Reset FONA"
