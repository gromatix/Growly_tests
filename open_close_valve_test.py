#!/usr/bin/env python

# Open/Close valve test for Growly 2.5
# Set proper Growly URL ('gurl' variable) to open in browser for test

import time
import datetime
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

gurl = 'http://'+sys.argv[2]+'/'
gcntr = int(sys.argv[1])+1		# global counter of tests

# gurl = 'http://192.168.0.1/'
browser = webdriver.Firefox()
browser.get(gurl)
color = browser.find_element_by_id("valve_9").get_attribute("fill")	#get current color of valve in UI
if (color=="green"):
	expcolor="red"		# next color to be expected
else:
	expcolor="green"

oldtime = datetime.datetime.now()
gts = datetime.datetime.now()	# test script start time
diffs = {}
tdiff = 0		# time difference
pcntr = 0		# passed tests counter
fcntr = 0		# failed tests counter
tocntr = 0		# counter of timeouts
dt = 0			# delta time
while (gcntr>0):
	browser.find_element_by_id("valve_9").click()		# click on valve 9 in UI
	dt = 0
	ts = datetime.datetime.now()
	while (color!=expcolor and dt<10):			# while color not changed and timeout not reched
		dt = (datetime.datetime.now()-ts).total_seconds()			# count timeout
		color = browser.find_element_by_id("valve_9").get_attribute("fill")	# get current color of element
	tdiff = (datetime.datetime.now()-oldtime).total_seconds()
	dts = str(round(dt,1))
	if dts in diffs:
		diffs[dts]+=1
	else:
		diffs[dts] = 1
	oldtime = datetime.datetime.now()
	print("[ Test "),
	print(int(sys.argv[1])-gcntr+1),
	print(" ]"),
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
		print(bcolors.OKGREEN + "Test Passed" + bcolors.ENDC)
		if (expcolor=="green"):
			expcolor="red"
		else:
			expcolor="green"
	else:
		print(bcolors.FAIL + "Test failed!" + bcolors.ENDC)
		fcntr+=1
	gcntr-=1

print("Test execution time statistics (seconds : times)")
for key in diffs:
	print(key),
	print(" : "),
	print(diffs[key])

print("Total: "),
print(sys.argv[1])
print("Failed: "),
print(fcntr)
print("Passed: "),
print(pcntr)
print("Total script execution time: "),
print(datetime.datetime.now()-gts)
