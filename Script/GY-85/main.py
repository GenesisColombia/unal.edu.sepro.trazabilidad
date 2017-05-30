# -*- coding: utf-8 -*-
from multiprocessing import Process
import math

import sys
import argparse
import file_writer
import stdout_writer
from stdout_writer import StdoutWriter
from sensor_reader import SensorReader
from file_writer import FileWriter


sensor_reader = SensorReader()
writer = StdoutWriter('/home/pi/Documents/SEPRO/Script/',1)

sensor_reader.set_sensor_listener(writer)
print ("Inclinacion ° \nYZ              XZ")
while True:

    # Consumer/producer architecture: the SensorReader is the producer, reading data from sensors,
    # and the FileWriter is the consumer.
    # We use multiprocessing.Process instead of threading.Thread because the latter would also cause
    # the other thread to slow down due to Global Interpreter Lock.

    # reset this because sensor_reader.start_reading() might execute before file_writer.start_write_loop()
    process = Process(target=writer.start_write_loop)
    process.start()

    sensor_reader.start_reading()
