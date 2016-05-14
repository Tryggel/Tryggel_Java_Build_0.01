#!/usr/bin/env python
#
import json
import arrow
import requests
from time import sleep

import sys

import mysql.connector
from datetime import time, date, timedelta, datetime
import os, time


def handelError ():
	e = sys.exc_info()[0]
	patch = "/home/ec2-user/"
	filename = "neurio-log.txt"
	logfile = open(patch+filename,'a+')
	print ("%s;%s\n" % (e,datetime.now()))
	logfile.write ("%s;%s\n" % (e,datetime.now()))
	logfile.close ()

def set_TZ():
	os.environ['TZ'] = 'Europe/Berlin'
	time.tzset()


def SendDataSQL (kWtime, kW):
	
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

	add_reading = ("INSERT INTO `mess_all`.`neurio_1` "
               "(`idnew_table`, `new_tablecol`) "
               "VALUES (%s, %s)")
	# Insert new employee
				

				#2015-12-01 12:12:11
				
	data_readings = (kWtime,kW)
	cursor.execute(add_reading, data_readings)

	# execute SQL query using execute() method.

	# Make sure data is committed to the database
	cnx.commit()
	cursor.close()
	cnx.close()


#Transforms Neurio's datetime string to normal datetime standart. 
def NioDate (values):
				year = int (values[0:4])
				month = int (values[5:7])
				day = int (values[8:10])
				hour = int (values[11:13])
				min = int (values[14:16])
				sec = int (values[17:19])
				msec = int (values[20:23])
				t = time(hour, min,sec)
				d = date(year,month,day)
				t = time(hour, min,sec)
				d = date(year,month,day)
				return datetime.combine(d, t)

def GettingData():
	my_tocken = "Bearer AIOO-2knTltHtDrEmwPlxq_q-acjnUVEjLJ_qEnnlz0XoMsiCEhry6r4PhiyBS1_b8I26YjMgBU0mrABwjBcbRTDIY1Xomkq-eQF5AyxGZghRK2emG-pqtCRADFkbGds6UGYaQSr1oSP-A5LEOywEaEcmAessuRTmR9rQKY_E2dwA5OvLa_jcVRhu1wk8Nozau-P6ovdrqtOS9T1izsyyS2we0uX4KUsb-tDeFZPdRqW9gUkIpkrhzEq8doe9EIvC1IrCWjn36vd"
	nio_url_live='https://api.neur.io/v1/samples/live?sensorId='
	nio_sens_id='0x0000C47F510181D6'
	url = nio_url_live+nio_sens_id

	lastDate = ''
	set_TZ()
	while True:
		#geting the values from Neurio DB
		res = requests.get(
			url,
			headers={
			'Authorization': my_tocken,
			'Content-Type': 'application/json'
			}
		)
		#print ("Statuscode: %s" % res.status_code)
		jstr = json.dumps(res.json())
		
		#Transforming from Json into Python array
		jstr = json.loads(jstr)
		i = 0
		n = len(jstr)
		i = n +0-1
		#print i 
		#Problem solved: Write only the values, which are still not in the system
		while i > -1 and jstr[i]['timestamp'] != lastDate :
			i -= 1
		if jstr[i]['timestamp'] == lastDate: 
			i -= 1
		else:
			i = 0
			n = len(jstr)
			i = n +0-1
		#print ("New Reading is starting. Starting from:" + i)

		#http://stackoverflow.com/questions/10140281/how-to-find-out-whether-a-file-is-at-its-eof
		#for chunk in iter(lambda: fp.read(n), ''):
		#	process(chunk)
		
		#Starting to check the values
		while i > -1:
				#print(my_list[i])
				print ('N:%d;\tW:%d;\tT:%s' %(
					i
					,jstr[i]['consumptionPower']
					#,jstr[i]['timestamp'][0:10]
					,jstr[i]['timestamp']
					#,impuls
					#,energy*1000
					)
				)
				#print ('\t;Cond:{0:3d}mW'.format(int(energy*1000)))
				SendDataSQL(jstr[i]['timestamp'],jstr[i]['consumptionPower'])
				i -= 1
		#print (impulses)
		lastDate = jstr[0]['timestamp']
		sleep(60)
		
	#for oneMess in jstr:
	#	print (neMess['consumptionPower'])
	f.close()
	
	#i = 0

def main():
	while True:
		try:
			set_TZ()
			GettingData()
		except: 
			handelError ()
			sleep(5)
			

main()

