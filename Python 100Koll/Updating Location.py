
import requests

TOKEN = "a4829e66-20d4-47b8-b922-2827cc8395a2"
LOCATION = "610c820b-6b6d-40b7-a44e-e83a3d0cdd8f"
url = "https://api-nordic.eon.se/neo/api/100koll/v1/OlingoProvider.svc/Locations('" + LOCATION + "')"
url = "https://api-nordic.eon.se/neo/api/100koll/v1/OlingoProvider.svc/Locations"

body = {
			"name": "Test",
			"tariff": 10.0,
			"agreementType": "G",
			"impKwh": 1000,
			"podNumber ": "1001234",
			"address": {
				"street1": "Gata 1 A",
				"city": "Stad",
				"postalCode": "1234",
				"country": "SE"
			}
		}
		
headers = {
    'authorization': "Bearer " + TOKEN,
    'content-type': "application/json"
    }

response = requests.request("POST", url, headers=headers, data=json.dumps(body))
print(response.text)