import json
import requests
from time import sleep

import mysql.connector
from datetime import time, date, timedelta, datetime

#tocken = "Mi45MTExOkVvbnN2ZXJpZ2Ux"
#plugid = "101171"

try:
	cnx  = mysql.connector.connect(host='megatrenddb.ctcmpabozwdk.us-west-2.rds.amazonaws.com'
							,user='tryggel'
							,password='megatrend15'
							,database=''
							)

	# prepare a cursor object using cursor() method
	cursor = cnx.cursor()
		
	get_data = ("SELECT `w` FROM `mess_all`.`koll_all` WHERE sensorID = 101177 AND `datetime` >= `2016-04-21` AND `w` != `0` LIMIT 0, 100000")
					  ("VALUES (%s)")
	data_readings = (w)
		
	cursor.execute(get_data, data_readings)
		
	cursor.close()
	cnx.close()
	f = open('myfile','w')
	f.write(getValues() + 'hi there\n') # python will convert \n to os.linesep
	f.close() # you can omit in most cases as the destructor will call it
		
		
		
except mysql.connector.Error as err:
	print("Something went wrong: {}".format(err))
		