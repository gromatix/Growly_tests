#!/usr/bin/env python

# Open/Close valve test for Growly 2.5
# Set proper Growly URL ('gurl' variable) to open in browser for test

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime

gurl = 'http://192.168.0.1/'
browser = webdriver.Firefox()
browser.get(gurl)
color = browser.find_element_by_id("valve_9").get_attribute("fill")	#get current color of valve in UI
if (color=="green"):
	expcolor="red"		# next color to be expected
else:
	expcolor="green"

oldtime = datetime.datetime.now()
tdiff = 0	# time difference
gcntr = 0	# global counter of tests
pcntr = 0	# passed tests counter
fcntr = 0	# failed tests counter
tocntr = 0	# counter of timeouts
dt = 0		# delta time
while 1:
	browser.find_element_by_id("valve_9").click()		# click on valve 9 in UI
	dt = 0
	ts = datetime.datetime.now()
	while (color!=expcolor and dt<10):			# while color not changed and timeout not reched
		dt = (datetime.datetime.now()-ts).total_seconds()			# count timeout
		color = browser.find_element_by_id("valve_9").get_attribute("fill")	# get current color of element
	tdiff = (datetime.datetime.now()-oldtime).total_seconds()		
	oldtime = datetime.datetime.now()
	print(gcntr),
	print(" Passed: "),
	print(pcntr),
	print("/ Failed: "),
	print(fcntr),
	print(" TO: "),
	print(tocntr),
	print(" >>> "),
	print("Time spent: "),
	print(tdiff)
	if (dt>5):
		tocntr+=1
	print(datetime.datetime.now())
	if (color==expcolor):
		pcntr+=1
		print("Test OK\n")
		if (expcolor=="green"):
			expcolor="red"
		else:
			expcolor="green"
	else:
		print("Test failed!\n")
		fcntr+=1
	gcntr+=1
