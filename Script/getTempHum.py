import sys
import AM2302

sensor = AM2302.AM2302
pin = 23;

humidity, temperature = AM2302.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1);
def write():
	return AM2302.read_retry(sensor, pin)
