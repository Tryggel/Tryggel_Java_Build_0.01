def KollGetRefreshToken(pod_id, access_token, refresh_token, expires_in):
	
# Open database connection
#db = mysql.connector.connect(host='megatrenddb.ctcmpabozwdk.us-west-2.rds.amazonaws.com'
print ("SQL: Starting function...")


data = (pod_id, x["access_token"], x["refresh_token"], x["expires_in"])

cnx  = mysql.connector.connect(host='megatrenddb.ctcmpabozwdk.us-west-2.rds.amazonaws.com'
						,user='tryggel'
						,password='megatrend15'
						,database=''
						)
cursor = cnx.cursor()

add_reading = ("SELECT refresh_token, pod_id, ID FROM mess_all.koll_token t "
				"WHERE ID = (SELECT max(ID) FROM mess_all.koll_token WHERE t.pod_id = pod_id)"
				)
cursor.execute(add_reading)
								
readings = []			
for (refresh_token, pod_id, ID) in cursor:
	print (refresh_token, pod_id, ID)
	readings.insert(len(readings), (refresh_token, pod_id))
cursor.close()
cnx.close()
	

#cnx.commit()
cursor.close()
cnx.close()
	
import sys, time
import inspect
from datetime import time, date, timedelta, datetime

def nsys():
	sys._getframe().f_code.co_name
	wait1 = datetime.now()
	print sys._getframe().f_code.co_name
	print (datetime.now() - wait1).total_seconds()


def nins():
	wait1 = datetime.now()
	print inspect.stack()[0][3]
	print (datetime.now() - wait1).total_seconds()