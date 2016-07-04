#Refreshing Tokens from 100koll
#Get code: https://api-nordic.eon.se/neo/oauth/v2/authorization?client_id=tryggel&response_type=code&scope=100koll

import requests
import urllib
import urlparse
import warnings
import requests
import json
import datetime
import mysql.connector
from datetime import time, date, timedelta, datetime
import sys
import os, time
from time import sleep
from slackclient import SlackClient

def handelError ():
	e = sys.exc_info()
	token = "xoxp-12755663922-12785724403-56506604960-7ad7e8bf9d"
	sc = SlackClient(token)
	sc.api_call(
		"chat.postMessage", channel="C1NET49QE", text=e,
		username='pybot', icon_emoji=':robot_face:'
		)
	patch = "/home/ec2-user/"
	filename = "log.txt"
	logfile = open(patch+filename,'a+')
	print ("Following Error: %s;%s\n" % (e,datetime.now()))
	logfile.write ("%s;%s\n" % (e,datetime.now()))
	logfile.close ()

def set_TZ():
	os.environ['TZ'] = 'Europe/Berlin'
	time.tzset()

#Returns the refresh token
def SQL_GetRefreshTokens():
	wait1 = datetime.now()
	# Open database connection
	#db = mysql.connector.connect(host='megatrenddb.ctcmpabozwdk.us-west-2.rds.amazonaws.com'
	cnx  = mysql.connector.connect(host='megatrenddb.ctcmpabozwdk.us-west-2.rds.amazonaws.com'
							,user='tryggel'
							,password='megatrend15'
							,database=''
							)
	cursor = cnx.cursor()
	add_reading = ("SELECT refresh_token, pod_id, expires_in, time_got "
					"FROM (SELECT * FROM mess_all.koll_token "
					"ORDER BY ID DESC) AS t GROUP BY pod_id")

	#data = (pod_id,)
	cursor.execute(add_reading)
	tokens = []
	for (refresh_token, pod_id, expires_in, time_got) in cursor:
		refresh_token = refresh_token
		time1 = time_got
		expires_in = expires_in
		#print "Got the token %s %s %s %s" % (refresh_token, pod_id, expires_in, time_got)
		tokens.insert(len(tokens), (refresh_token, pod_id, expires_in, time_got))
	#time2 = datetime.now()
	#timed = time2 - time1 
	#timewait = timed.total_seconds()
	cursor.close()
	cnx.close()
	#print expires_in
	#print timewait
	#print "The token will expire in %ds." % (expires_in - timewait)
	print "Function %s was finished in: %ss" % (sys._getframe().f_code.co_name,(datetime.now() -wait1).total_seconds())
	return tokens

def CommitNewToken(new_tokens):
	
# Open database connection
#db = mysql.connector.connect(host='megatrenddb.ctcmpabozwdk.us-west-2.rds.amazonaws.com'
	wait1 = datetime.now()
	cnx  = mysql.connector.connect(host='megatrenddb.ctcmpabozwdk.us-west-2.rds.amazonaws.com'
							,user='tryggel'
							,password='megatrend15'
							,database=''
							)
	cursor = cnx.cursor()
	for new_token in new_tokens:
		add_reading = ("INSERT INTO mess_all.koll_token "
				"(pod_id, access_token, refresh_token, expires_in) "
				"VALUES (%s, %s, %s, %s)")
		data = (new_token["pod_id"],new_token["access_token"],new_token["refresh_token"],new_token["expires_in"])
		cursor.execute(add_reading, data)
	cnx.commit()
	cursor.close()
	cnx.close()
	print "Function %s was finished in: %ss" % (sys._getframe().f_code.co_name,(datetime.now() -wait1).total_seconds())


#Returns a json with new tokens
def GetNewToken(tokens):
	# Hide deprecation warnings.
	
	wait1 = datetime.now()
	warnings.filterwarnings('ignore', category=DeprecationWarning)
	CLIENT_SECRET = "3Cw59$ngUGf#576Dja#y"
	CLIENT_ID = "tryggel"
	SCOPE = "100koll"
	TOKEN_URL = "https://api-nordic.eon.se/neo/oauth/v2/token"
	GRANT_TYPE = "refresh_token"

	#Getting the refresh_token
	new_tokens = []
	#Building the request body.
	for refresh_token in tokens: 
		REFRESH_TOKEN = refresh_token[0]
		oauth_args = dict(
			client_id     = CLIENT_ID,
			client_secret = CLIENT_SECRET,
			grant_type    = GRANT_TYPE,
			scope = SCOPE,
			refresh_token = REFRESH_TOKEN
			)
						  
		#urlencode of the body.
		oauth_curl_cmd = ['curl', TOKEN_URL + "?"+ urllib.urlencode(oauth_args)]

		response = requests.post(TOKEN_URL, data = oauth_args)
		jstr = json.dumps(response.json())
		jstr = json.loads(jstr)
		jstr["pod_id"] = refresh_token[1]
		jstr["time_got"] = datetime.now()
		new_tokens.insert(len(new_tokens), jstr)
		print "The new refresh_token:%s" % jstr["refresh_token"]

	print "Function %s was finished in: %ss" % (sys._getframe().f_code.co_name,(datetime.now() -wait1).total_seconds())
	return new_tokens

def main():
	try:
		#Setting the right time zone
		set_TZ()
		wait1 = datetime.now()
		refresh_tokens = SQL_GetRefreshTokens()
		new_tokens = GetNewToken(refresh_tokens)
		CommitNewToken(new_tokens)
		#rsp_json = GetNewToken(pod_id)
		#CommitNewToken(pod_id, rsp_json["access_token"], rsp_json["refresh_token"], rsp_json["expires_in"])
		#print rsp_json
		
		print "Function %s was finished in: %ss" % (sys._getframe().f_code.co_name,(datetime.now() -wait1).total_seconds())
		sleep(60*60*2-60*10)
	except: 
		handelError ()
		sleep(5)

set_TZ()
while True: 		
	main()	
