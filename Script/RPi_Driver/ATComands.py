import serial 
from time import sleep

# Definitions Global Variables
true =1;
false =0;
ERROR_PWR = "ERROR EN EJECUCION DEL GPS, NO SE ENCUENTRA ALIMENTADO";
ERROR_SIGNAL = "ERROR EN EJECUCION DEL GPS, NO TIENE SENYAL DE SATELITES";
ERROR_NETWORK = "ERROR EN CONEXION CON LA RED";
ERROR_ANS = "ERROR LA RESPUESTA NO ES LA ESPERADA";
ERROR_COMM = "ERROR COMUNICACION SERIAL"

def Send(port,str_TX,str_RX,lines):
	# Definitions to keep the information
	i=0;
	RX_info = '';

	port.write(str_TX);					# Send string to module
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
	if (sizeRX==0):
		return ERROR_COMM
	if(str_TX!='AT+CIFSR\n' and str_TX!='AT+CGATT=0\n'):
		for i in range(sizeRX-sizestr,sizeRX):
			try:
				Check += RX_info[i];
			except IndexError:
				Check = 'null'
		if(RX_info == "+PDP: DEACT\r\n\r\nERROR\r\n"):
			print "Existen problemas con la read, se volvera a reiniciar el proceso";
			return ERROR_NETWORK;
		elif(Check != str_RX):
			print ("No son iguales los strings");
			return ERROR_ANS;
	return RX_info

def KeepGPS(port):
	Keep = Send(port,'AT+CGNSINF\r\n','OK\r\n',3);
	while (Keep==ERROR_ANS):
		Send(port,'AT\r\n','OK\r\n',3);
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
	print "info-->",info,"<--",len(info);
	# Keeping date
	if len(info)<10:
		return 0,0,0
	try:
		day = int(info[10]+info[11]);
	except IndexError:
		day = 1
	try:
		hour = int(info[12]+info[13]);
		hour -= 5;
	except IndexError:
		hour=1
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
	getLat = true;
	getLon = true;
	getAlt = true;
	Lat = '';
	Lon = '';
	Alt = '';
	for i in range(0,30):
		if(info[23]==','):
			return ERROR_SIGNAL,'\0','\0';
		elif(info[i+23]!=',' and getLat):
			Lat += info[i+23];
		elif(info[i+23]!=',' and getLon):
			Lon += info[i+23];
		elif(info[i+23]!=',' and getAlt):
			Alt += info[i+23];
		elif(info[i+23]==',' and not getLon):
			getAlt = false;
		elif(info[i+23]==',' and not getLat):
			getLon = false;
		else:		 
			getLat = false;
	return Date,Lat,Lon,Alt;

def ShutGSM(port):
	Send(port,'AT+CIPSHUT\n','SHUT OK\r\n',1);
	Send(port,'AT+CGATT=0\n','OK\r\n',4);

def SendInfo(port,URL):
	port.write('AT+CIPSEND\n');
	port.readline();
	port.write(URL);
	for i in range(0,30):
		line = port.readline();
		print line,line.find("CLOSED");
		if (line.find("CLOSED")!=-1):
			print "Breack, conn closed"
			break
		if (line.find("DEACT")!=-1 or line.find("R14.18")!=-1):
			return "pwr"
