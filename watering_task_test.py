#!/usr/bin/env python

# Open/Close valve test for Growly 2.5
# Set proper Growly URL ('gurl' variable) to open in browser for test
# first test case works with no output valve selected. Input only

import time
import datetime
import sys
import collections
from selenium import webdriver
from selenium.webdriver.common.by import By


print("Growly 2v5: Watering Task test")
print("==============================")
print("")



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

out_tube_id = "svg_valve_6_tube"
gurl = 'http://'+sys.argv[2]+'/'
tests_amount = int(sys.argv[1])		# global counter of tests
watering_timeout = 30			# watering task recognized as failed, if no valve close within 'watering_timeout' seconds
gts = datetime.datetime.now()		# script start time
diffs = {}				# frequencies of start-to-valveopen delays
diffs2 = {}				# frequencies of watering task durations

# gurl = 'http://192.168.0.1/'
browser = webdriver.Firefox()
browser.get(gurl)

browser.find_element_by_id(out_tube_id).click()
browser.find_element_by_xpath('//b[@onClick="svg_dialog_watering_task_ss_plus()"]').click();
browser.find_element_by_xpath('//b[@onClick="svg_dialog_watering_task_ss_plus()"]').click();
browser.find_element_by_xpath('//b[@onClick="svg_dialog_watering_task_ss_plus()"]').click();

gcntr = 0
fcntr = 0
pcntr = 0




while (gcntr<tests_amount):
	print("Test " + str(gcntr+1))                                                          
	browser.find_element_by_id(out_tube_id).click()		# click on valve 9 in UI
	browser.find_element_by_id("svg_valve_9_tube").click()
        browser.find_element_by_xpath('//div[@onClick="svg_dialog_watering_task_start();"]').click();
	time.sleep(1)
        browser.find_element_by_xpath('//div[@onClick="svg_dialogs_close();"]').click();
	ts = datetime.datetime.now()
	# wait until input valve opened
	color = "red"
	print("Waiting task to start")
	dt = 0
	while (color=="red" and dt<watering_timeout):
		color = browser.find_element_by_id("valve_9").get_attribute("fill")
		dt = (datetime.datetime.now()-ts).total_seconds()
	dts = str(round(dt,1))
	if dts in diffs:
		diffs[dts]+=1
	else:
		diffs[dts] = 1
	print("Input valve opened after"),
	print(str(dt)),
	print("sec from start command")
	print("------------------------------");
	

	color = "green"
	dt = 0
	while (color=="green" and dt<watering_timeout):
		print("."),
		color = browser.find_element_by_id("valve_9").get_attribute("fill")
		dt = (datetime.datetime.now()-ts).total_seconds()
		time.sleep(1)
	print("")
	dts = str(round(dt))
	if dts in diffs2:
		diffs2[dts]+=1
	else:
		diffs2[dts] = 1
	if ((dt+5)>watering_timeout):
		# failed test case, due to timeout
		print(bcolors.FAIL + "timeout exceeded" + bcolors.ENDC)
		fcntr+=1
	else:
		# watering finished within timeout defined
		print(bcolors.OKGREEN + "Watering finished within timeout" + bcolors.ENDC)
		pcntr+=1
	print("Watering task " + str(gcntr+1) + " duration: "),
	print(dt)
	print("============================================")
        gcntr+=1

odiffs = collections.OrderedDict(sorted(diffs.items()))
odiffs2 = collections.OrderedDict(sorted(diffs2.items()))
print("=== Waterring task test statistics ===")
print("Delays between click on START button and [input valve opened]")
for key in odiffs:
	print(key),
	print(" : "),
	print(odiffs[key])

print("Delays between [input valve opened] and [input valve closed]")
for key in odiffs2:
	print(key),
	print(" : "),
	print(odiffs2[key])

print("")
print("Total: "),
print(sys.argv[1])
print("Failed: "),
print(fcntr)
print("Passed: "),
print(pcntr)
print("Total script execution time: "),
print(datetime.datetime.now()-gts)
