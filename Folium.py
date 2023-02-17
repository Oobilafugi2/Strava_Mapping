import folium
import requests
import urllib3
import polyline

# just getting rid of error warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# getting a token
auth_url = "https://www.strava.com/oauth/token"

# accessing activity
activities_url = "https://www.strava.com/api/v3/athlete/activities"

# json formatted data for personalized Strava authentication
payload = {
    'client_id': "101716",
    'client_secret': 'ae2715725ab2d1d18c9253f51e43bf13f8a10821',
    'refresh_token': '2e13f8670c06209846ecb4ac934da368860e038e',
    'grant_type': "refresh_token",
    'f': 'json'
}

# update the auth_url with the payload and store it in res, single out the new access token and print to verify
print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
# print("Access Token = {}\n".format(access_token))

# requesting to get data from activities using the refreshed access key
header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 10, 'page': 1}
my_dataset = requests.get(activities_url, headers=header, params=param).json()

# print(my_dataset[2]['map']['summary_polyline'])

polylines = []

for i in range(len(my_dataset)):
    route = polyline.decode(my_dataset[i]['map']['summary_polyline'])
    polylines.append(route)

# print(polylines[0])

m = folium.Map(location=[37.9101, -122.0652])


for i in range(len(polylines)):
    if polylines[i] != None:
        my_Polyline = folium.PolyLine(locations=polylines[i],weight=3)
        m.add_child(my_Polyline)

m.save(r"C:\Users\KevinJ\Strava_Mapping\index.html")
