import serial 

def Confirmation(port, str_send,str_recieve):
	port.write(b str_send);


# Access Serial port Raspberry Pi3
ser = serial.Serial('/dev/ttyS0',9600);

# Send Initial comands
ser.write(b'AT');
Confirmation(ser,'AT\n','OK\r\n');
Confirmation(ser,'AT+CGNSPWR=1\n','OK\r\n');
Confirmation(ser,'AT+CGNSSEQ="RMC"\n','OK\r\n');


ser.write(b'AT+CGNSINF\n');


Confirmation(ser,'AT+CGNSPWR=0','OK\r\n');
Confirmation(ser,'AT','OK\r\n');

