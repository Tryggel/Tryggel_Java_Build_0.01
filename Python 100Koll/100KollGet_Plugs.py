#!/usr/bin/env python
import json
import arrow
import requests
from time import sleep

import mysql.connector
from datetime import time, date, timedelta, datetime

#tocken = "Mi45MTExOkVvbnN2ZXJpZ2Ux"
#plugid = "101171"

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
	print ("%s;%s\n" % (e,datetime.now()))
	logfile.write ("%s;%s\n" % (e,datetime.now()))
	logfile.close ()

	
def DevicesWattNow (Authorization):
	koll_url_live = 'https://stagingapi.eon.se/eonapi/ODataProvider.svc/KwStreamLive'	
	url = koll_url_live
	try:
		res = requests.get(
			url
			,headers={
			'Authorization': Authorization,
			'Content-Type': 'application/json',
			'Accept': 'application/json'
			}
			,verify=False
		)
	
	except:
		print("Wrong answer from device API")
		return 0
	res = requests.get(
			url
			,headers={
			'Authorization': Authorization,
			'Content-Type': 'application/json',
			'Accept': 'application/json'
			}
			,verify=False
	)
	
	jstr = json.dumps(res.json())
	jstr = json.loads(jstr)
	
	try:
		return jstr['d']['results']	
	except:
		print("Wrong answer from device API")

	
def KollSendDataSQL (w,SensorID,date):
	
	# Open database connection
	#db = mysql.connector.connect(host='megatrenddb.ctcmpabozwdk.us-west-2.rds.amazonaws.com'
	try:
		cnx  = mysql.connector.connect(host='megatrenddb.ctcmpabozwdk.us-west-2.rds.amazonaws.com'
							,user='tryggel'
							,password='megatrend15'
							,database=''
							)

		# prepare a cursor object using cursor() method
		cursor = cnx.cursor()
		#DATETIME values in 'YYYY-MM-DD HH:MM:SS' format

		add_reading = ("INSERT INTO `mess_all`.`koll_all` "
				   "(`w`, `SensorID`, `datetime`) "
				   "VALUES (%s, %s, %s)")
					
		data_readings = (w,SensorID,date)
		cursor.execute(add_reading, data_readings)

		# execute SQL query using execute() method.
		# Make sure data is committed to the database
		cnx.commit()
		cursor.close()
		cnx.close()
	except mysql.connector.Error as err:
		print("Something went wrong: {}".format(err))
		patch = "/home/ec2-user/"
		filename = "sqllogkoll.txt"
		logfile = open(patch+filename,'a+') 
		logfile.write ('%s;%s' % (err,datetime.now()))
		datetime.now().ToString("%h")

def GettingData():
	set_TZ()
	w = 0
	timewait =0.0
	#List of plags with respective tokens
	list_devices = [[101171], [101177, 101176, 101175, 101174]]
	list_token = ['Mi45MTExOkVvbnN2ZXJpZ2Ux', 'Mi45MTEyOkVvbnN2ZXJpZ2Ux']

	while True:
		time1 = datetime.now()
		i = 0
		wait1 = time1
		#Call for every token
		while i < len(list_token): 
			wait1 = datetime.now()
			w = DevicesWattNow(list_token[i])
			if w <> 0:
				print ("%ss\tdone: requesting values." % ((datetime.now() -wait1).total_seconds()))
				wait1 = datetime.now()
				for device in w:
					#Send the values only for devices to SQL
					if device['deviceId'] in list_devices[i]:
						KollSendDataSQL(device['kw'],device['deviceId'],wait1)
				print ("%ss\tdone: send to SQL." % ((datetime.now() -wait1).total_seconds()))
				i=i+1
		
		#Waiting requested time till the next call
		time2 = datetime.now()
		timed = time2 - time1
		timewait = 10 - timed.total_seconds()
		timewait = max(timewait, 0)
		wait1 = datetime.now()
		sleep(timewait)
		print ("%s\tdone: waiting."  % ((datetime.now() -wait1).total_seconds()))

def main():
	try:
		set_TZ()
		GettingData()
	except: 
		handelError ()
		sleep(5)
		main()	
		
main()



