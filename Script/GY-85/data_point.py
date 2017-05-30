import math

def trunc(s):
    if len(s) > 5:
        return s[:6]
    else:
        return s


def format(val):
    return trunc(str(val))


class DataPoint:
    """
    Data point from a single sensor
    """

    def __init__(self, x=0.0, y=0.0, z=0.0, YZ=0.0, XZ=0.0, time=0.0, sensor_type=''):
        self.x = x
        self.y = y
        self.z = z

	try:
		self.YZ = math.degrees(math.atan(y/z))
	except ZeroDivisionError:
		self.YZ = 0
        try:
                self.XZ = math.degrees(math.atan(x/z))
        except ZeroDivisionError:
                self.XZ = 0
        self.time = time
        self.sensor_type = sensor_type

    def __str__(self):
        decimals = int(((self.time - int(self.time)) * 10000)) / 10000.0
        time_str = str(int(self.time) + decimals)
        return format(self.YZ) + ' ' + format(self.XZ)

    @staticmethod
    def from_str(serialized):
        comps = serialized.split(',')
        if len(comps) != 5:
            return None
        x = float(comps[1])
        y = float(comps[2])
        z = float(comps[3])
        try:
                YZ = math.degrees(math.atan(y/z))
        except ZeroDivisionError:
                YZ = 0
        try:
                XZ = math.degrees(math.atan(x/z))
        except ZeroDivisionError:
                XZ = 0
        time = float(comps[4])
        sensor_type = comps[0]
        return DataPoint(x, y, z, YZ, XZ, time, sensor_type)
