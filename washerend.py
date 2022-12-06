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


def getDifference():
	global xo
	global yo
	global zo
	global difference
	x = Xaccel(i2c.scan()[i])
	y = Yaccel(i2c.scan()[i])
	z = Zaccel(i2c.scan()[i])
	difference = 100*((x-xo)**2 + (y-yo)**2 + (z-zo)**2)**(0.5)
	xo = x 
	yo = y 
	zo = z 
	time.sleep(0.2)
	return difference

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

		xo = Xaccel(i2c.scan()[i])
		yo = Yaccel(i2c.scan()[i])
		zo = Zaccel(i2c.scan()[i])
		cycleComplete = False

		getDifference()
		print("difference is "+str(difference))

		if difference < threshold:
			for j in range(10):
				getDifference()
				if difference > threshold:
					cycleComplete = False
					break
				time.sleep(1)
				print("slept for a second")
				if j == 9:
					cycleComplete = True
					print("tested 10 rounds")

		if cycleComplete == True:
			print("machine has probably reliably stopped")
			cycleComplete = False

		while True:
			getDifference()
			if difference > threshold:
				break

			time.sleep(1)

		

except KeyboardInterrupt:
	i2c.deinit()
	pass

