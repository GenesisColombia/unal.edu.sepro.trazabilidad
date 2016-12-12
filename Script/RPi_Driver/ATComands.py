import serial 
from time import sleep

# Definitions Global Variables
true =1;
false =0;
ERROR_PWR = "ERROR EN EJECUCION DEL GPS, NO SE ENCUENTRA ALIMENTADO";
ERROR_GPS_SIGNAL = "ERROR EN EJECUCION DEL GPS, NO TIENE SENYAL DE SATELITES";

def Send(port,str_TX,str_RX,lines):
	# Definitions to keep the information
	i=0;
	RX_info = '';

	port.write(str_TX);				# Send string to module
	sleep(0.020);
	TX_info = port.readline();			# Always the module transmits the string which we send
	while i<lines:
		RX_info += port.readline();
		i+=1;
	print TX_info;
	print RX_info;
	
	# Checking of the last line of RX_info
	i=0;
	Check = '';
	sizeRX = len(RX_info);
	sizestr = len(str_RX);	
	for i in range(sizeRX-sizestr,sizeRX):
		Check += RX_info[i];

	if(Check != str_RX):
		print ("No son iguales los strings");
	return RX_info

def KeepGPS(port):
	Keep = Send(port,'AT+CGNSINF\r\n','OK\r\n',3);
	info = '';
	initial = false;
	# Keep in a new array the important information 
	for i in range(0,len(Keep)):
		if(Keep[i]=='1'):
			initial = true;
			info += Keep[i];
		elif(Keep[i]=='\n'):
			initial = false;
		elif(initial):
			info += Keep[i];
		elif(Keep[i]=='0'):
			return ERROR_PWR,'\0','\0';
	print info;
	# Keeping date
	day = int(info[10]+info[11]);
	hour = int(info[12]+info[13]);
	hour -= 5;
	if(hour<0):
		hour = 24 + hour;
		day = day -1;
	Date = "";
	for i in range(0,18):
		if(i<6):
			Date += info[i+4];
		if(i>9):
			Date += info[i+4];
		elif(i==6):
			if(day<10):
				s_day = '0'+str(day);
			else:
				s_day = str(day);
			Date += s_day;
		elif(i==9):
			if(hour<10):
				s_hour = '0'+str(hour);
			else:
				s_hour = str(hour);
			Date += s_hour;
	
	#Keeping Latitude and Longitude
	Lat = '';
	Lon = '';
	for i in range(0,21):
		if(info[23]==','):
			return ERROR_GPS_SIGNAL,'\0','\0';
		elif(i<10):
			Lat += info[i+23];
		else:
			Lon += info[i+23];
	return Date,Lat,Lon;
