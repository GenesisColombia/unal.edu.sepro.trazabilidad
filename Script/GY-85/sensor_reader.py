import random
import time
import math
from adxl345.i2c import ADXL345
from data_point import DataPoint

class SensorReader:
    """
    Reads data from accelerometer, gyroscope and compass
    """

    def __init__(self):
        self.__stopped = True
        self.samples_per_sec = 0
        self.accelerometer = ADXL345(alternate=True)
        self.accelerometer.set_data_rate(800)
        self.accelerometer.set_range(16, True)

    def set_sensor_listener(self, listener):
        self.listener = listener

    def start_reading(self):
        self.accelerometer.power_on()

        self.__stopped = False
        self.last_sec = self.current_sec()
        self.__samples_in_sec = 0
        self.started_ms = self.current_millis_frac()
        self.read_samples = 0

        while not self.__stopped:

            reading = self.__read_accelerometer()

            curr_sec = self.current_sec()
            if self.last_sec != curr_sec:
                secs = curr_sec - self.last_sec
               # print('Samples read: ' + str(
               #     self.read_samples) + ' (samples/sec: ' +
               #       str(self.samples_per_sec) + ")")
                self.samples_per_sec = self.__samples_in_sec / secs
                self.__samples_in_sec = 0
                self.last_sec = curr_sec

            self.__samples_in_sec += 1

            self.read_samples += 1

            # pass to consumer
            if not self.listener.on_sensor_data_changed(reading):
                self.__stopped = True
                print("Stopping sensor reader")

    def __read_accelerometer(self):
        acc_reading = DataPoint()
        acc_reading.sensor_type = 'acc'
        acc = self.accelerometer.read_data()
	if acc:
        	acc_reading.x = acc[0]
        	acc_reading.y = acc[1]
        	acc_reading.z = acc[2]
        try:
                acc_reading.YZ = math.degrees(math.atan(acc_reading.y/acc_reading.z))
        except ZeroDivisionError:
                acc_reading.YZ = 0
        try:
                acc_reading.XZ = math.degrees(math.atan(acc_reading.x/acc_reading.z))
        except ZeroDivisionError:
                acc_reading.XZ = 0
        acc_reading.time = self.current_millis_frac() - self.started_ms
        return acc_reading

    def __sensor_to_read(self):
        """

        :return: Which sensor to read from in the current iteration (based on read_samples)
        """
        return 'acc'

        # TODO uncomment to also read from other sensors, if needed
        # remainder = self.read_samples % 16
        # if remainder == 0 or remainder == 11:
        #     return 'gyr'
        # elif remainder == 6:
        #     return 'comp'
        # else:
        #     return 'acc'

    @staticmethod
    def current_millis_frac():
        return time.time() * 1000

    def current_sec(self):
        return int(round(time.time()))

    def stop(self):
        self.__stopped = True

    def is_stopped(self):
        return self.__stopped
