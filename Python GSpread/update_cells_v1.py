import gspread
import json
from time import sleep
from datetime import time, date, timedelta, datetime

import os, time

#from sqlobject import *
from oauth2client.service_account import ServiceAccountCredentials


def set_TZ():
	os.environ['TZ'] = 'Europe/Berlin'
	time.tzset()

def last_updated(wks):
		
	lastUpdate = ("Updated: %s" % datetime.now())
	wks.update_acell("A2",lastUpdate)
	
def value_to_date (value):
	
	date_object = datetime.strptime(value, '%m/%d/%Y')
	return date_object
	
	
#Opens our worksheet (Token and the name are given)
def open_wks ():

	scope = ['https://spreadsheets.google.com/feeds']

	#The key need to be in the same folder as the script
	credentials = ServiceAccountCredentials.from_json_keyfile_name('gkey.json', scope)

	gc = gspread.authorize(credentials)

	wks = gc.open("Larm Centralen View").sheet1
	return wks

#Updates the wks for the life activities depending on the daytime
def check_activity (wks):
	okValue = "OK"
	waitValue = "..waiting"
	checkTime = [10 ,15 ,20, 24]

	cell_list = wks.range('B4:E4')
	i = 0
	#Current hour
	curretHour = datetime.now().timetuple()[3]
	last_updated(wks)
	
	for oneCell in cell_list:
		#looks for the first wait cell 
		print("Checking the values %s and %s" % (oneCell.value, waitValue))
		if oneCell.value == waitValue:
			#if the time already passed, check it as OK
			if curretHour >= checkTime[i]:
				oneCell.value = okValue
				wks.update_cells(cell_list)
			return
		i = i + 1	

#Just moves the rows down	
def moving_rows (wks):
	cell_list = wks.range('A4:E10')
	waitValue = "..waiting"
	preCells = [0,0,0,0,0,0,0,0,0,0]
	for oneCell in cell_list:
		#Saving the values of the cell
		tempCell = oneCell.value
		#Replacing it with the value of the previous cell
		oneCell.value = preCells[oneCell.col]
		#If it was a first cell, replacing it with the new value
		if preCells[oneCell.col] == 0 :
			if oneCell.col == 1:
				oneCell.value = datetime.now().date()
			else:
				oneCell.value = waitValue
				
		#Making this cell into the previous cell
		preCells[oneCell.col] = tempCell
	wks.update_cells(cell_list)
	


def animation (wks):
	while True:
		time1 = datetime.now()
		check_activity(wks)
		
		ddays = (datetime.now() - value_to_date (wks.acell("A4").value))
		print ("Days check: %s" % ddays)
		if ddays.days >= 1:
			print ("Moving rows: %s" % datetime.now().time())
			moving_rows (wks)
			print ("Moving rows finished: %s" % datetime.now().time())
		
		timed = datetime.now() - time1
		timewait = 10 - timed.total_seconds()
		timewait = max(timewait, 0)
		wait1 = datetime.now()
		print ("waiting %s sec" % timewait)
		sleep(timewait)
	
	
	
def update_cells ():

	wks = open_wks ()
	#Select the list of the cols with Dates
	#cell_list = wks.range('A4:A10')


	while True:
		#checking the live checks
		timew = datetime.now()
		check_activity(wks)
		dtime = datetime.now() - timew
		print ("waiting for live checks: %s" % dtime)
		
		#Getting the rang from wks
		timew = datetime.now()
		cell_list = wks.range('A4:A10')
		dtime = datetime.now() - timew
		print ("waiting for gspread: %s" % dtime)
		
		#Shifting cells, if the time have passed
		preCell = 0.0
		time1 = datetime.now()
		for oneCell in cell_list:
			if preCell == 0.0:
				preCell = datetime.now()
				
			bufCell  = oneCell.value
			oneCell.value = preCell
			preCell = bufCell 
			print ("updating %s" % preCell)
		timew = datetime.now()
		wks.update_cells(cell_list)
		dtime = datetime.now() - timew
		print ("updating cells: %s" % dtime)

		#Waiting requested time till the next call
		timed = datetime.now() - time1
		timewait = 5 - timed.total_seconds()
		timewait = max(timewait, 0)
		wait1 = datetime.now()
		print ("waiting %s sec" % timewait)
		sleep(timewait)
	open_wks ()



def main():
	set_TZ()
	wks = open_wks ()
	animation (wks)
	#moving_rows ()
	#update_cells ()


main()


	   

