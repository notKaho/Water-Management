#sudo rfcomm bind 0 00:18:E4:40:00:06

import RPi.GPIO as GPIO
import time
import datetime
import serial
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import httplib, urllib2

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

Relay = 5
Buzzer = 23
x = 0

GPIO.setup(Relay, GPIO.OUT)
GPIO.setup(Buzzer, GPIO.OUT)


api_key = '29D5HF22CFXPBJHI'
base_url = "http://api.thingspeak.com/update?api_key=%s" % api_key

#ser = serial.Serial('/dev/ttyUSB0', 9600) # UART
ser = serial.Serial('/dev/rfcomm0') # BT
#data = ""

def email():
	now = datetime.datetime.now()
	currenttime = now.strftime("%Y-%m-%d %H:%M:%S")
	
	msg = MIMEMultipart('alternative')
	
	msg['Subject'] = "Flood Control System Alert" " | " ""+ currenttime + "" " | " "ACTIVATED"
	msg['From'] = "group5aaenotification@gmail.com"
	msg['To'] = "chadgroup5@gmail.com"
	
	text = "Please do not reply to this automated message."
	
	html = """\
	<html>
	 <head></head>
	<body>
		<p style="color: darkred;">Please do not reply to this automated message.</p>
	</body>
	</html>
	"""
	# *HTML* Formatting of the Message
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')
	
	msg.attach(part1)
	msg.attach(part2)
	
	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.ehlo()
	server.login('group5aaenotification@gmail.com', 'Group5AAE')
	server.sendmail('group5aaenotification@gmail.com', 'chadgroup5@gmail.com', msg.as_string())
	print("Email Sent")
	server.quit()
	
	
def thingspeak():
	try:
		url = base_url+"&field3=%d"%(ldr_variable)+"&field4=%d"%(rgb_variable) \
		+"&field1=%d"%(t_variable)+"&field2=%d"%(h_variable)
		f = urllib2.urlopen(url)
		print('Uploading Data...')
		f.close()
	except:
		print('Pass')
		pass
	

while 1:
	data = ser.readline()
	#print (data)
	
	a = data.split(",")
	#print (a)
	
	ir_string = a[0]
	ldr_string = a[1]
	t_string = a[2]
	h_string = a[3]
	rgb_string = a[4]
	
	print ('IR Sensor = '+ ir_string)
	print ('LDR Sensor = '+ldr_string)
	print ('Temperature = '+t_string)
	print ('Humidity = '+h_string)
	print ('RGB State = '+rgb_string)
	
	ir_variable = int(ir_string)
	ldr_variable = int(ldr_string)
	t_variable = float(t_string)
	h_variable = float(h_string)
	rgb_variable = int(rgb_string)
	
	if ir_variable == 1:
		GPIO.output(Relay, 0)
		GPIO.output(Buzzer, 0)
		x = 0
		
	else:
		GPIO.output(Relay, 1)
		GPIO.output(Buzzer, 1)
		if x == 0:
			for x in range(0,2):
				if x == 1:
					email()
					pass
				if x == 2:
					pass
					
	thingspeak()
