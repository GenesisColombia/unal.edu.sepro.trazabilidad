# D.J.Whale
# http://blog.whaleygeek.co.uk/raspberry-pi-rfid-tag-reader
#
import rfid
import requests, time

while True:

  # wait for a card to be detected as present
  print "Waiting for a card..."
  rfid.waitTag()
  print("Card present")

  # This demo only uses Mifare cards
  if not rfid.readMifare():
	print("This is not a mifare card")
	file=open('/home/pi/Documents/SEPRO/Script/id.txt','w')
	file.truncate()
	file.write("ERROR")
	print "ERROR";
	time.sleep(2)
	file.truncate()
	file.close()
  else:
	# look up the unique ID to see if we recognise the user
	uid = rfid.getUniqueId();
	typ = rfid.getTypeName();    
	print(uid)
	file=open('/home/pi/Documents/SEPRO/Script/id.txt','w')
	file.truncate()
	info = "";
	info = str(uid) + " " + typ; # Mandar por el archivo de texto el numero y el tipo de tarjeta 
	print info;
	file.write(info);
	file.close()

  # wait for the card to be removed
  print("Waiting for card to be removed...")
  rfid.waitNoTag()
  print("Card removed")

# END
