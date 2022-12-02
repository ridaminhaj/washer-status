from machine import Pin
from machine import I2C
from binascii import hexlify
import time

from mqttclient import MQTTClient
import network
import sys

i2c = I2C(1,scl=Pin(22),sda=Pin(23),freq=400000)


for i in range(len(i2c.scan())):
	print(hex(i2c.scan()[i]))


def WHOAMI(i2caddr):
	whoami = i2c.readfrom_mem(i2caddr,0x0F,1)
	print(hex(int.from_bytes(whoami,"little")))

# def Temperature(i2caddr):
# 	temperature = i2c.readfrom_mem(i2caddr,0x20,2)
# 	if int.from_bytes(temperature,"little") > 32767:
# 		temperature = int.from_bytes(temperature,"little")-65536
# 	else:
# 		temperature = int.from_bytes(temperature,"little")
# 	print("%4.2f" % ((temperature)/(256) + 25))

def Zaccel(i2caddr):
	zacc = int.from_bytes(i2c.readfrom_mem(i2caddr,0x2C,2),"little")
	if zacc > 32767:
		zacc = zacc -65536
	print("%4.2f" % (zacc/16393))
	return abs(zacc/16393)

def Xaccel(i2caddr):
	xacc = int.from_bytes(i2c.readfrom_mem(i2caddr,0x28,2),"little")
	if xacc > 32767:
		xacc = xacc -65536
	print("%4.2f" % (xacc/16393))
	return abs(xacc/16393)

def Yaccel(i2caddr):
	yacc = int.from_bytes(i2c.readfrom_mem(i2caddr,0x2A,2),"little")
	if yacc > 32767:
		yacc = yacc -65536
	print("%4.2f" % (yacc/16393))
	return abs(yacc/16393)


# def getDifference():
# 	global xo
# 	global yo
# 	global zo
# 	x = Xaccel(i2c.scan()[i])
# 	y = Yaccel(i2c.scan()[i])
# 	z = Zaccel(i2c.scan()[i])
# 	difference = 100*((x-xo)**2 + (y-yo)**2 + (z-zo)**2)**(0.5)
# 	xo = x 
# 	yo = y 
# 	zo = z 
# 	time.sleep(0.2)
# 	return difference

def CycleCompleteMessage(feedName):
	mqtt.publish(feedName, "Cycle Complete")
	return 0

buff=[0xA0]
i2c.writeto_mem(i2c.scan()[i],0x10,bytes(buff))
i2c.writeto_mem(i2c.scan()[i],0x11,bytes(buff))
time.sleep(0.1)

difference = 0
threshold = 50

try:
	while(1) :
		WHOAMI(i2c.scan()[i])
		# Temperature(i2c.scan()[i])
		xo = Xaccel(i2c.scan()[i])
		yo = Yaccel(i2c.scan()[i])
		zo = Zaccel(i2c.scan()[i])

		while difference < threshold:
			x = Xaccel(i2c.scan()[i])
			y = Yaccel(i2c.scan()[i])
			z = Zaccel(i2c.scan()[i])
			difference = 100*((x-xo)**2 + (y-yo)**2 + (z-zo)**2)**(0.5)
			print("diff "+str(difference))
			xo = x 
			yo = y 
			zo = z 

			time.sleep(0.2)

		print("threshold reached")
		break



# try:
# 	raise IndexError("This is an IndexError")
# 	while(1) :
# 		WHOAMI(i2c.scan()[i])
# 		# Temperature(i2c.scan()[i])

# 		xo = Xaccel(i2c.scan()[i])
# 		yo = Yaccel(i2c.scan()[i])
# 		zo = Zaccel(i2c.scan()[i])
# 		cycleComplete = False

# 		getDifference()

# 		if difference < threshold:
# 			for i in range(10):
# 				getDifference()
# 				if difference > threshold:
# 					cycleComplete = False
# 					break
# 			cycleComplete = True

# 		if cycleComplete == True:
# 			CycleCompleteMessage(washer)

# 		print("threshold reached")
# 		break


# wlan = network.WLAN(network.STA_IF)
# wlan.active(True)
# ip = wlan.ifconfig()[0]
# if ip == '0.0.0.0':
#     print("no wifi connection")
#     sys.exit()
# else:
#     print("connected to WiFi at IP", ip)

# # Set up Adafruit connection
# adafruitIoUrl = 'io.adafruit.com'
# adafruitUsername = 'ridaminhaj'
# adafruitAioKey = 'aio_STAP89P0iQWllOCDQub5OlVkKwjx'

# # Define callback function
# def sub_cb(topic, msg):
#     print((topic, msg))

# # Connect to Adafruit server
# print("Connecting to Adafruit")
# mqtt = MQTTClient(adafruitIoUrl, port='1883', user=adafruitUsername, password=adafruitAioKey)
# time.sleep(0.5)
# print("Connected!")

# feedName = "ridaminhaj/feeds/washer"
# testMessage = "Cycle Complete"


# try:
# 	while(1) :
# 		WHOAMI(i2c.scan()[i])
# 		xo = Xaccel(i2c.scan()[i])
# 		yo = Yaccel(i2c.scan()[i])
# 		zo = Zaccel(i2c.scan()[i])

# 		while True:
# 			x = Xaccel(i2c.scan()[i])
# 			y = Yaccel(i2c.scan()[i])
# 			z = Zaccel(i2c.scan()[i])
# 			difference = 100*((x-xo)**2 + (y-yo)**2 + (z-zo)**2)**(0.5)
# 			if difference  threshold:
# 				time.sleep(1)
# 				difference2 = 0
# 				xo = x
# 				yo = y
# 				zo = z 
# 				x = Xaccel(i2c.scan()[i])
# 				y = Yaccel(i2c.scan()[i])
# 				z = Zaccel(i2c.scan()[i])
# 				difference2 = 100*((x-xo)**2 + (y-yo)**2 + (z-zo)**2)**(0.5)
# 				if difference2 < threshold:
# 					#perform feed activity
					
# 					mqtt.publish(feedName, testMessage)
					

# 			print("diff "+str(difference))
# 			xo = x 
# 			yo = y 
# 			zo = z 

# 			time.sleep(0.2)

		

except KeyboardInterrupt:
	i2c.deinit()
	pass


# wlan = network.WLAN(network.STA_IF)
# wlan.active(True)
# ip = wlan.ifconfig()[0]
# if ip == '0.0.0.0':
#     print("no wifi connection")
#     sys.exit()
# else:
#     print("connected to WiFi at IP", ip)

# # Set up Adafruit connection
# adafruitIoUrl = 'io.adafruit.com'
# adafruitUsername = 'ridaminhaj'
# adafruitAioKey = 'aio_STAP89P0iQWllOCDQub5OlVkKwjx'

# # Define callback function
# def sub_cb(topic, msg):
#     print((topic, msg))

# # Connect to Adafruit server
# print("Connecting to Adafruit")
# mqtt = MQTTClient(adafruitIoUrl, port='1883', user=adafruitUsername, password=adafruitAioKey)
# time.sleep(0.5)
# print("Connected!")

# # This will set the function sub_cb to be called when mqtt.check_msg() checks
# # that there is a message pending
# mqtt.set_callback(sub_cb)

# # Send test message
# feedName = "ridaminhaj/feeds/washer"
# testMessage = "Cycle Complete"
# # testMessage = "1"
# mqtt.publish(feedName,testMessage)
# print("Published {} to {}.".format(testMessage,feedName))

# mqtt.subscribe(feedName)

# # For one minute look for messages (e.g. from the Adafruit Toggle block) on your test feed:
# for i in range(0, 60):
#     mqtt.check_msg()
#     time.sleep(1)
