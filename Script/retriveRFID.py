file= open('/home/pi/Documents/SEPRO/Script/id.txt','r+')
for line in file:
        print line
#Delete information in Text
file= open('/home/pi/Documents/SEPRO/Script/id.txt','w')

file.truncate()
