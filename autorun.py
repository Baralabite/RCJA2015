"""
This program runs automatially when the Hexapod turns on.
"""

import RPi.GPIO as GPIO
import rpyc
import time
import os
import threading

conn = None
app = None
up = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(25, GPIO.OUT)

"""def getPushSignature():
	while GPIO.input(24) == 1:
		time.sleep(0.05)
	a = time.time()
	while GPIO.input(24) == 0:
		time.sleep(0.05)
	b = time.time()
	return b-a"""

def getPushSignature():
	while GPIO.input(24) == 1:
		pass
	a = time.time()
	while GPIO.input(24) == 0:
		pass
	time.sleep(0.1)
	while GPIO.input(24) == 0:
		pass
	b = time.time()
	return b-a

def beep_():
	threading.Thread(target=beep).start()

def beep():
	for x in range(100):
		GPIO.output(25, True)
		time.sleep(0.001)
		GPIO.output(25, False)
		time.sleep(0.001)

if __name__ == "__main__":
	time.sleep(10)
	beep_()
	conn = rpyc.connect("localhost", 12345)
	app = conn.root.exposed_get_app()
	app.cacheRoutine()
	while True:
		sig = getPushSignature()
		print(sig)
		if conn == None:
			#try:
			conn = rpyc.connect("localhost", 12345)
			app = conn.root.exposed_get_app()
			app.cacheRoutine()
			#except:
			#print("Robot server not currently running.")
		if sig > 1 and sig < 5:
			if up == False:
				app.se.playAction("standUp")
				up = True
				print("Standing up...")
			else:
				app.se.playAction("sitDown")
				up = False
				print("Sitting down...")
		elif sig > 10:
			os.system("sudo shutdown -h now")
		else:
			beep_()
			app.rcjaRoutine()
		time.sleep(1)
		

