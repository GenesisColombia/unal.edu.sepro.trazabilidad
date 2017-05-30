file= open('/home/pi/Documents/SEPRO/Script/gyr','r+')
for line in file:
	print line
#Delete information in Text
file= open('/home/pi/Documents/SEPRO/Script/gyr','w')

file.truncate()
