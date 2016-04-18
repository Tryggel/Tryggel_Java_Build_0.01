import gspread
import json
from time import sleep
from datetime import time, date, timedelta, datetime

#from sqlobject import *
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

#The key need to be in the same folder as the script
credentials = ServiceAccountCredentials.from_json_keyfile_name('gkey.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open("Larm Centralen View").sheet1

#Select the list of the cols with Dates
#cell_list = wks.range('A4:A10')

while True:
	timew = datetime.now()
	cell_list = wks.range('A4:A10')
	dtime = datetime.now() - timew
	print ("waiting for gspread: %s" % dtime)
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

	
	
	
print (values_kw)
#json_str = json.dumps(data)



	   

