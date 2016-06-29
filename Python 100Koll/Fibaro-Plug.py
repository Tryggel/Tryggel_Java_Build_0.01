#!/usr/bin/env python
import json
import arrow
import requests
from time import sleep

import mysql.connector
from datetime import time, date, timedelta, datetime

import sys
import os, time
def set_TZ():
	os.environ['TZ'] = 'Europe/Berlin'
	time.tzset()


def handelError ():
	e = sys.exc_info()[0]
	patch = "/home/ec2-user/"
	filename = "100koll-plug-log.txt"
	logfile = open(patch+filename,'a+')
	print ("Following Error: %s;%s\n" % (e,datetime.now()))
	logfile.write ("%s;%s\n" % (e,datetime.now()))
	logfile.close ()

	
def DevicesWattNow (Authorization):
	fibaro_server = "127.0.0.1"
	koll_url_live = 'http://' + fibaro_server + ':8083/ZWaveAPI/Run/devices[3].instances[0].commandClasses[49].data[4].val.value'	
	url = koll_url_live
	res = requests.get(
		url
		,headers={
		'Authorization': Authorization,
		}
	)
	jstr = json.dumps(res.json())
	jstr = json.loads(jstr)
	print jstr
	#print jstr.replace(".",",")
	return jstr

	
def KollSendDataSQL (w,SensorID,date):
	
	# Open database connection
	#db = mysql.connector.connect(host='megatrenddb.ctcmpabozwdk.us-west-2.rds.amazonaws.com'
	cnx  = mysql.connector.connect(host='megatrenddb.ctcmpabozwdk.us-west-2.rds.amazonaws.com'
						,user='tryggel'
						,password='megatrend15'
						,database=''
						)
	# prepare a cursor object using cursor() method
	cursor = cnx.cursor()
	#DATETIME values in 'YYYY-MM-DD HH:MM:SS' format
	add_reading = ("INSERT INTO `mess_all`.`fibaro` "
	   "(`w`, `SensorID`, `datetime`) "
	   "VALUES (%s, %s, %s)")
				
	data_readings = (w,SensorID,date)
	cursor.execute(add_reading, data_readings)
	# execute SQL query using execute() method.
	# Make sure data is committed to the database
	cnx.commit()
	cursor.close()
	cnx.close()

def GettingData():
	set_TZ()
	w = 0
	timewait =0.0
	#List of plags with respective tokens
	list_token = ['Basic YWRtaW46YW5kYW1vMTU=']
	device_id = "104"
	while True:
		time1 = datetime.now()
		i = 0
		wait1 = time1
		#Call for every token
		while i < len(list_token): 
			wait1 = datetime.now()
			w = DevicesWattNow(list_token[i])
			print ("%ss\tdone: requesting values." % ((datetime.now() -wait1).total_seconds()))
			wait1 = datetime.now()
			#Send the values only for devices to SQL
			KollSendDataSQL(w,device_id,wait1)
			print ("%ss\tdone: w send to SQL." % ((datetime.now() -wait1).total_seconds()))
			i=i+1
		
		#Waiting requested time till the next call
		time2 = datetime.now()
		timed = time2 - time1
		timewait = 1 - timed.total_seconds()
		timewait = max(timewait, 0)
		wait1 = datetime.now()
		sleep(timewait)
		print ("%s\tdone: waiting."  % ((datetime.now() -wait1).total_seconds()))

def main():
	#try:
		set_TZ()
		GettingData()
	#except: 
	#	handelError ()
	#	sleep(5)

while True: 		
	main()
	
	



