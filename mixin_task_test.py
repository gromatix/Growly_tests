#!/usr/bin/env python

# Mix-IN task test for Growly 2.6
# Usage: python mixin_task_test.py <tests_count> <growly_ip> <dosing> <aftermix>
#   where: tests_count - how many tests we want to run
#          growly_ip - an IP address of Growly device
#	   dosing - seconds to run doser
#	   aftermix - seconds to mix, after doser stopped

def add_dosing(browser, duration):
	for x in range(int(duration/10)):
		browser.find_element_by_id("svg_dialog_mixin_task_dosing_btn_plus_x").click();
	for x in range(int(duration%10)):
		browser.find_element_by_id("svg_dialog_mixin_task_dosing_btn_plus").click();

def add_aftermix(browser, duration):
	for x in range(int(duration/10)):
		browser.find_element_by_id("svg_dialog_mixin_task_aftermix_btn_plus_x").click();
	for x in range(int(duration%10)):
		browser.find_element_by_id("svg_dialog_mixin_task_aftermix_btn_plus").click();


import time
import datetime
import sys
import collections
from selenium import webdriver
from selenium.webdriver.common.by import By


print("   Growly 2v6 Mix-IN Task test")
print("=================================")
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

# user defined variables
doser_id = "svg_doser_1"
gurl = 'http://'+sys.argv[2]+'/'	# Growly URL, constructed from an IP (<growly_ip>) 
tests_amount = int(sys.argv[1])		# how many tests to perfom (<tests_count>)
dosing = int(sys.argv[3])		# dosing duration
aftermix = int(sys.argv[4])		# aftermix duration

# internal variables
gcntr = 0	# global counter
fcntr = 0	# failed tests counte
pcntr = 0	# passed tests counter

test_timeout = dosing + aftermix + 20	# task recognized as failed, if no valve close within 'watering_timeout' seconds
gts = datetime.datetime.now()		# script start time
diffs_start = {}				# 
diffs_dosing = {}				#
diffs_aftermix = {}				#

browser = webdriver.Firefox()
browser.get(gurl)

# set MixIN task settings
browser.find_element_by_id(doser_id).click()
time.sleep(1)

# add 4 seconds of dosing
print("Setting " + str(dosing) + " seconds of dosing")
add_dosing(browser, dosing)

# add 2 seconds aftermix
print("Setting " + str(aftermix) + " seconds of aftermix")
add_aftermix(browser, aftermix)

# close Mix-IN dialog
browser.find_element_by_id("svg_dialog_mixin_task_btn_close").click()

time.sleep(1)

while (gcntr<tests_amount):
	print(" ============ Test " + str(gcntr+1) + " ============")

	browser.find_element_by_id(doser_id).click()
	time.sleep(1)

	# start task
	browser.find_element_by_id("svg_dialog_mixin_task_btn_start").click()

	test_start = datetime.datetime.now()	# test start

	color = "red"
	delta_time = 0

	# start counter, wait until doser starts
	while (color=="red" and delta_time<test_timeout):
		color = browser.find_element_by_id(doser_id).get_attribute("fill")
		delta_time = (datetime.datetime.now()-test_start).total_seconds()


	# doser started
	dosing_started_time = datetime.datetime.now()

	delta_time_string = str(round(delta_time,1))

	if delta_time_string in diffs_start:
		diffs_start[delta_time_string] += 1
	else:
		diffs_start[delta_time_string] = 1

	print("Task start delay: "),
	print(delta_time)

	# close Mix-IN dialog
	browser.find_element_by_id("svg_dialog_mixin_task_btn_close").click()	

	# wait, until doser stops
	color = "green"
	while (color=="green" and delta_time<test_timeout):
		color = browser.find_element_by_id(doser_id).get_attribute("fill")
		delta_time = (datetime.datetime.now()-dosing_started_time).total_seconds()


	# dosing stopped, start counting lenght of aftermix
	aftermix_started_time = datetime.datetime.now()

	# store the time of dosing
	delta_time_string = str(round(delta_time,1))
	if delta_time_string in diffs_dosing:
		diffs_dosing[delta_time_string] += 1
	else:
		diffs_dosing[delta_time_string] = 1

	print("Dosing duration: "),
	print(delta_time)
	color = "green"
	while (color=="green" and delta_time<test_timeout):
		color = browser.find_element_by_id("psi_pump_svg").get_attribute("fill")
		delta_time = (datetime.datetime.now()-aftermix_started_time).total_seconds()
	print("Aftermix duration: "),
	print(delta_time)
	# aftermix finished, store its lenght
	delta_time_string = str(round(delta_time,1))
	if delta_time_string in diffs_aftermix:
		diffs_aftermix[delta_time_string] += 1
	else:
		diffs_aftermix[delta_time_string] = 1

	test_time = datetime.datetime.now() - test_start
	if (test_time.total_seconds() > test_timeout):
		# failed test case, due to timeout
		print(bcolors.FAIL + "timeout exceeded" + bcolors.ENDC)
		fcntr+=1
	else:
		# watering finished within timeout defined
		print(bcolors.OKGREEN + "Test finished within timeout" + bcolors.ENDC)
		pcntr+=1

	print("Test  " + str(gcntr+1) + " duration: "),
	print(test_time)
	print("=================================")
        gcntr+=1
	time.sleep(1)		# wait a second between tasks

odiffs_start = collections.OrderedDict(sorted(diffs_start.items()))
odiffs_dosing = collections.OrderedDict(sorted(diffs_dosing.items()))
odiffs_aftermix = collections.OrderedDict(sorted(diffs_aftermix.items()))

print("=== Mix-IN task test statistics ===")
print("Delays between click on START button and [input valve opened]")
for key in odiffs_start:
	print(key),
	print(" : "),
	print(odiffs_start[key])

print("Delays between [doser started] and [doser stopped]")
for key in odiffs_dosing:
	print(key),
	print(" : "),
	print(odiffs_dosing[key])

print("Delays between [doser stopped] and [main pump stopped]")
for key in odiffs_aftermix:
	print(key),
	print(" : "),
	print(odiffs_aftermix[key])

print("")
print("Total: "),
print(sys.argv[1])
print("Failed: "),
print(fcntr)
print("Passed: "),
print(pcntr)
print("Total script execution time: "),
print(datetime.datetime.now()-gts)

