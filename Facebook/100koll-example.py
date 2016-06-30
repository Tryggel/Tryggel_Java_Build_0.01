
import requests
access_token = "758b0a9d-45e3-41e0-ad47-d6880c368136"
headers = {"Authorization": "bearer " + access_token}
api = "https://qa-api-nordic.eon.se/api/hemmakoll/v3"
response = requests.get(api+"/OlingoProvider.svc/Devices", headers=headers)
#me_json = response.json()
#print me_json['name']
print response
