import sys
import AM2302

sensor = AM2302.AM2302
pin = 23;

def write():
	return AM2302.read_retry(sensor, pin)
