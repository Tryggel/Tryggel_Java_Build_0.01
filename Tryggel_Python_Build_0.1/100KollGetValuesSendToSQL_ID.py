#!/usr/bin/env python
#
import json
import arrow
import requests
from time import sleep

import mysql.connector
from datetime import time, date, timedelta, datetime

#tocken = "Mi45MTExOkVvbnN2ZXJpZ2Ux"
#plugid = "101171"

def PlugWattNow (PlugID, Authorization):
	koll_url_live = 'https://stagingapi.eon.se/eonapi/ODataProvider.svc/KwStreamLive?$filter=deviceId eq '
	nio_sens_id = PlugID
	
	url = koll_url_live + nio_sens_id
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
	
	print (jstr['d']['results'][0]['kw'])
	return jstr['d']['results'][0]['kw']
	
	
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
				   "(`w`, `SensorID`, `date`) "
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
		logfile.write ('%s;%s' % (err,time.now()))

def main():
	tocken = "Mi45MTExOkVvbnN2ZXJpZ2Ux"
	plugid = "101172"
	w = 0
	timewait =0.0
	while True:
		time1 = datetime.now()
		wait1 = time1
		w = PlugWattNow(plugid,tocken)
		print ("%ss\tdone: requesting values." % ((datetime.now() -wait1).total_seconds()))
		#print ("oDelta%s"%oDelta)
		wait1 = datetime.now()
		KollSendDataSQL(w,plugid,wait1)
		print ("%ss\tdone: send to SQL." % ((datetime.now() -wait1).total_seconds()))
		print ('W:%s;\tT:%s;' %(
			w 	
			,datetime.now()
			)
		)
		time2 = datetime.now()
		timed = time2 - time1
		timewait = 60 - timed.total_seconds()
		timewait = max(timewait, 0)
		wait1 = datetime.now()
		sleep(timewait)
		print ("%s\tdone: waiting."  % ((datetime.now() -wait1).total_seconds()))
		

		
main()



