from __future__ import print_function
import os
from os import listdir
from os.path import isfile, join
import multiprocessing
from multiprocessing import Queue
from time import sleep
import math
stop = multiprocessing.Value("i", 0)
XZ_ant=[0]
YZ_ant=[0]
atipico=False


class StdoutWriter:
    def __init__(self, path='~/Documents/SEPRO/Script/',nth_sample=1):
        """

        :param path: Directory in which files will be written
        """

        # for multiprocessing
        self.__buffer = Queue()
        self.path = path
        self.fname = None
        self.nth_sample = nth_sample

    def _write_header(self):
        self.__f.write("XZ,YZ\n")
	#print ("heder")

    def on_sensor_data_changed(self, data_point):
        """
        Passes data to the consumer (consumer/producer architecture). Runs on producer process.
        :returns If the writer has been stopped
        """

        global stop

        if stop.value != 0:
            return False
        else:
            self.__buffer.put(data_point)
            return True

    def _write_sample(self, XZ, YZ):
        """
        :param sample: Writes a DataPoint to the file
        :return:
        """

        if self.fname is None:
            self._new_file()

        self.written += 1
	self.__f.seek(0)
	global XZ_ant
	global YZ_ant	
	global atipico
	if self.file_size() == 0 :
		
		XZ_1 = XZ_ant.pop() 
        	YZ_1 = YZ_ant.pop()
		
        	if math.sqrt(math.pow(XZ_1-XZ,2))<2 and math.sqrt(math.pow(YZ_1-YZ,2))<2 :
			self.__f.write(str(round(XZ))+' '+str(round(YZ)))
			XZ_ant.append(XZ)
                        YZ_ant.append(YZ)
			atipico=False
			print ("Flie Written -> "+str(round(XZ,0))+' '+str(round(YZ,0)))
		elif (not atipico):
			self.__f.write(str(round(XZ_1))+' '+str(round(YZ_1)))
			XZ_ant.append(XZ)
			YZ_ant.append(YZ)
			atipico=True;
			print ("Flie Written -> "+str(round(XZ_1,0))+' '+str(round(YZ_1,0)))
		elif (atipico):
			self.__f.write(str(round(XZ))+' '+str(round(YZ)))
			XZ_ant.append(XZ)
                        YZ_ant.append(YZ)
			atipico=True
                        print ("Flie Written -> "+str(round(XZ,0))+' '+str(round(YZ,0)))
		sleep(0.9);
	#print ('\r')

    def start_write_loop(self):
        """
        Starts consumer loop that writes data points to a file. Runs on consumer process.
        """

        global stop
        stop.value = 0

        count = 0
	sumXZ=0
	sumYZ=0

        while True:
            # This obviously is a very naive implementation of the consumer (while loop instead of lock).
            # However, this already achieves the maximum sampling rate because the I2C communication with
            # the sensors is the bottleneck.
            if not self.__buffer.empty():
                data_point = self.__buffer.get()
		count +=1
		sumXZ += data_point.XZ
		sumYZ += data_point.YZ
		promXZ = (sumYZ/count)
		promYZ = (sumXZ/count)
		if count % self.nth_sample == 0:
	  	    #self._write_sample(promXZ,promYZ)
                    self._write_sample(data_point.XZ,data_point.YZ)
                    #print("raw-"+str(data_point))
		    #print("prom"+str(promXZ)+" "+str(promYZ)+"--->"+str(sumXZ)+"/"+str(count)+"--->"+str(sumYZ)+"/"+str(count))
                    sumXZ=0
                    sumYZ=0
                    promXZ=0
                    promYZ=0
                    count=1

    def file_size(self):
        """

        :return: Size of file in MB
        """
        return os.stat(join(self.path, self.fname)).st_size / 1000.0

    def _new_file(self):
        # Files are named 'recording_x' where x is a sequence number. Find the highest sequence number in the dir and add 1.
        #files_in_dir = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        #max_number = 0
        #for f in files_in_dir:
        #    if f.startswith('recording_'):
        #        number = int(f[10:])
        #        if number > max_number:
        #            max_number = number
        filename = 'gyr'
        self.__f = open(join(self.path, filename), 'w+')
	print ("file opened")
        #self._write_header()
        self.fname = filename
        self.written = 0

        print('Writing to file ' + join(self.path, filename))
