import drivers

temperature = 0;
humidity =0;
temperature, humidity = drivers.read();
print ("Temperature = %s *C" % temperature);
print ("Humidity = %s %" % humidity);
