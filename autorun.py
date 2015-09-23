"""
This program runs automatially when the Hexapod turns on.
"""

import RPi.GPIO as GPIO
import rpyc
import time
import os

conn = None
app = None
up = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def getPushSignature():
	while GPIO.input(24) == 1:
		time.sleep(0.05)
	a = time.time()
	while GPIO.input(24) == 0:
		time.sleep(0.05)
	b = time.time()
	return b-a


while True:
	sig = getPushSignature()
	print(sig)
	if conn == None:
		#try:
		conn = rpyc.connect("localhost", 12345)
		app = conn.root.exposed_get_app()
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
		app.rcjaRoutine()
	time.sleep(1)
		
def getPushSignature():
	while GPIO.input(24) == 1:
		pass
	a = time.time()
	while GPIO.input(24) == 0:
		pass
	b = time.time()
	return b-a
