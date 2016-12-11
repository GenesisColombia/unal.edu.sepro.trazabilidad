import RPi.GPIO as GPIO
from time import sleep

def read():
	# Definitions
	SENSOR_MAXCOUNT = 32000; 			# Magic number for Raspberry processor
	SENSOR_PULSES = 41;					# Number of Pulses when the information is sending

	# Define error constants.
	SENSOR_ERROR_TIMEOUT  = -1;
	SENSOR_ERROR_CHECKSUM = -2;


	Pin = 4;							# Pinout from Raspberry to out pin on AM2302	
	GPIO.setmode(GPIO.BCM) 				# Broadcom pin-numbering scheme
	
	# Return variables
	temperature = 0;
	humidity = 0;

	PulseCounts[SENSOR_PULSES*2]=0;
	GPIO.setup(Pin, GPIO.OUT), 			# First send the signal to recieve the information
	
	# Send pulse
	GPIO.output(Pin, GPIO.HIGH);
	sleep(0.5);
	GPIO.output(Pin, GPIO.LOW);
	sleep(0.020);

	# Read sensor - Recieving information
	GPIO.setup(Pin, GPIO.IN);
	for i in range(0,50):		
		a=0;
	count = 0;
	while GPIO.input(Pin)==1:
		count+=1;
		if count >= SENSOR_MAXCOUNT:
			return SENSOR_ERROR_TIMEOUT;
	
	# Record pulse widths for the expected result bits.
	for i in lim(0,SENSOR_PULSES*2,2):
		# Count how long pin is low and store in PulseCounts[i]
		while GPIO.input(Pin)==0:
			PulseCounts[i] += 1;		  
			if PulseCounts[i] >= SENSOR_MAXCOUNT:
				#Timeout waiting for response.
				return SENSOR_ERROR_TIMEOUT;
		
		# Count how long pin is high and store in PulseCounts[i+1]
		while GPIO.input(Pin)==1:
			PulseCounts[i+1] += 1;
			if PulseCounts[i+1] >= SENSOR_MAXCOUNT:
				# Timeout waiting for response.
				return SENSOR_ERROR_TIMEOUT;

	# Done with timing critical code, now interpret the results.


	# Compute the average low pulse width to use as a 50 microsecond reference threshold.
	# Ignore the first two readings because they are a constant 80 microsecond pulse.
	threshold = 0;
	for i in lim(2,SENSOR_PULSES*2,2):
		threshold += PulseCounts[i];

	threshold /= SENSOR_PULSES-1;

	data[5] = {0};
	for i in lim(3,SENSOR_PULSES*2,2):
		index = (i-3)/16;
		data[index] <<= 1;
		if PulseCounts[i] >= threshold:
			# One bit for long pulse.
			data[index] |= 1;
		# Else zero bit for short pulse.

	if data[4] == ((data[0] + data[1] + data[2] + data[3]) & 0xFF):
		# Calculate humidity and temp for the sensor.
		humidity = (data[0] * 256 + data[1]) / 10.0;
		temperature = ((data[2] & 0x7F) * 256 + data[3]) / 10.0;
		if data[2] & 0x80:
			temperature *= -1.0;
		return temperature,humidity;
	else:
		return SENSOR_ERROR_CHECKSUM;

# Range to a for
def lim(start, end, step):
    while start <= end:
        yield start
        start += step


