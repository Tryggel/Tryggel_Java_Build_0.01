import gspread
import json

from sqlobject import *
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('gkey.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open("Test_Consumption").sheet1

values_hms = wks.col_values(3)
values_kw = wks.col_values(1)

data = {

	'kw' : values_kw,
	'hms' : values_hms

}
json_str = json.dumps(data)



   

