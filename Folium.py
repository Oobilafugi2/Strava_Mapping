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
param = {'per_page': 50, 'page': 1}
my_dataset = requests.get(activities_url, headers=header, params=param).json()

# print(my_dataset[2])

# initialize folium map, set basemap and starting location
m = folium.Map(tiles='cartodbdark_matter', location=[37.9101, -122.0652])

# loop through the full dataset
for i in range(len(my_dataset)):

    # Separate runs and rides to give them each different properties
    if my_dataset[i]["type"] == 'Ride':
        
        # the "try" gets around activities that have no polyline
        # the block decodes the polyline into coordinates, and adds that and the activity name to the map
        try:
            route = polyline.decode(my_dataset[i]['map']['summary_polyline'])
            popup_text = my_dataset[i]['name']
            popup = folium.Popup(html=popup_text)
            my_Polyline = folium.PolyLine(locations=route,weight=3, popup=popup,)
            m.add_child(my_Polyline)
        except ValueError:
            print("no polyline")
    if my_dataset[i]["type"] == 'Run':
        try:
            route = polyline.decode(my_dataset[i]['map']['summary_polyline'])
            popup_text = my_dataset[i]['name']
            popup = folium.Popup(html=popup_text)
            my_Polyline = folium.PolyLine(locations=route,weight=3, color="red", popup=popup)
            m.add_child(my_Polyline)
        except ValueError:
            print("no polyline")

        
# pushes map to html file where it can be displayed
m.save(r"C:\Users\KevinJ\Strava_Mapping\index.html")
