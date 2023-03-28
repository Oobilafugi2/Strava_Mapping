import folium
import requests
import urllib3
import polyline

# just getting rid of error warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# getting a token
auth_url = "https://www.strava.com/oauth/token"

# access url for all personal activities
activities_url = "https://www.strava.com/api/v3/athlete/activities"

# access url for specific activities
maui_swim = "https://www.strava.com/api/v3/activities/8759766824"
sequoia = "https://www.strava.com/api/v3/activities/7677946114"
girona = "https://www.strava.com/api/v3/activities/5715725714"
maui_loop = "https://www.strava.com/api/v3/activities/6963333407"
pt_reyes_s = "https://www.strava.com/api/v3/activities/4633463489"
pt_reyes_b = "https://www.strava.com/api/v3/activities/4633474417"
pt_reyes_r = "https://www.strava.com/api/v3/activities/4633488814"
yosemite_b = "https://www.strava.com/api/v3/activities/5029170903"
yosemite_r = "https://www.strava.com/api/v3/activities/5029178170"
bay_1 = "https://www.strava.com/api/v3/activities/4555528709"
bay_2 = "https://www.strava.com/api/v3/activities/4556834648"
bay_3 = "https://www.strava.com/api/v3/activities/4557902905"


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
param = {'per_page': 200, 'page': 1}
my_dataset = requests.get(activities_url, headers=header, params=param).json()
maui_swim_data = requests.get(maui_swim, headers=header, params=param).json()
sequoia_data = requests.get(sequoia, headers=header, params=param).json()
girona_data = requests.get(girona, headers=header, params=param).json()
maui_loop_data = requests.get(maui_loop, headers=header, params=param).json()
pt_reyes_s_data = requests.get(pt_reyes_s, headers=header, params=param).json()
pt_reyes_b_data = requests.get(pt_reyes_b, headers=header, params=param).json()
pt_reyes_r_data = requests.get(pt_reyes_r, headers=header, params=param).json()
yosemite_b_data = requests.get(yosemite_b, headers=header, params=param).json()
yosemite_r_data = requests.get(yosemite_r, headers=header, params=param).json()
bay_1_data = requests.get(bay_1, headers=header, params=param).json()
bay_2_data = requests.get(bay_2, headers=header, params=param).json()
bay_3_data = requests.get(bay_3, headers=header, params=param).json()

# initialize folium map, set default map to blank so all the custom maps on top take precedent
m = folium.Map(tiles=None, location=[37.9101, -122.0652])
folium.raster_layers.TileLayer(tiles='cartodbdark_matter', name='Tapintoit').add_to(m)

# title_html = '''
#              <h3 align="center" style="font-size:20px"><b>Your map title</b></h3>
#              '''
# m.get_root().html.add_child(folium.Element(title_html))

# initialize layers where routes will be stored
fg_challenges = folium.FeatureGroup("Challenges")
fg_rides = folium.FeatureGroup("Cycling Training")
fg_runs = folium.FeatureGroup("Run Training")
fg_swims = folium.FeatureGroup("Swim Training")

# loop through the full personal activities dataset
for i in range(len(my_dataset)):
    # Separate runs, rides, and swims to give them each different properties
    if my_dataset[i]["type"] == 'Ride':
        
         # the "try" gets around activities that have no polyline
         # the block decodes the polyline into coordinates
         # gets name of activity and url for the popup, which opens in a new tab
        try:
            route = polyline.decode(my_dataset[i]['map']['summary_polyline'])
            popup_text = my_dataset[i]['name']
            popup_id = str(my_dataset[i]['id'])
            popup = "<a href=https://www.strava.com/activities/"+popup_id+" target=_blank> "+ popup_text +" </a>"

            # layer option
            folium.PolyLine(locations=route, weight=2, popup=popup).add_to(fg_rides)

            # non-layer option
            # my_Polyline = folium.PolyLine(locations=route,weight=3, popup=popup,)
            # m.add_child(my_Polyline)
        except ValueError:
            pass
        except KeyError:
            pass

    if my_dataset[i]["type"] == 'Run':
        try:
            route = polyline.decode(my_dataset[i]['map']['summary_polyline'])
            popup_text = my_dataset[i]['name']
            popup_id = str(my_dataset[i]['id'])
            popup = "<a href=https://www.strava.com/activities/"+popup_id+" target=_blank> "+ popup_text +" </a>"

            folium.PolyLine(locations=route, weight=2, color="red", popup=popup).add_to(fg_runs)
            
        except ValueError:
            pass
        except KeyError:
            pass

    if my_dataset[i]["type"] == 'Swim':
        try:
            route = polyline.decode(my_dataset[i]['map']['summary_polyline'])
            popup_text = my_dataset[i]['name']
            popup_id = str(my_dataset[i]['id'])
            popup = "<a href=https://www.strava.com/activities/"+popup_id+" target=_blank> "+ popup_text +" </a>"
        

            folium.PolyLine(locations=route, weight=2, color="green", popup=popup).add_to(fg_swims)
            
        except ValueError:
            pass
        except KeyError:
            pass


# this part is repetative and will get looped eventually, just doing this for now for the site
# takes data from specific activity request and does the same process as the loops above
# right now these are the tapintoit challenges   
maui_swim_route = polyline.decode(maui_swim_data['map']['summary_polyline'])    
popup_text = maui_swim_data['name']    
popup_id = str(maui_swim_data['id'])
popup = "<a href=https://www.strava.com/activities/"+popup_id+" target=_blank> "+ popup_text +" </a>"

folium.PolyLine(locations=maui_swim_route, weight=3, color="gold", popup=popup).add_to(fg_challenges)

sequoia_route = polyline.decode(sequoia_data['map']['summary_polyline'])    
popup_text = sequoia_data['name']    
popup_id = str(sequoia_data['id'])
popup = "<a href=https://www.strava.com/activities/"+popup_id+" target=_blank> "+ popup_text +" </a>"
folium.PolyLine(locations=sequoia_route, weight=3, color="gold", popup=popup).add_to(fg_challenges)

girona_route = polyline.decode(girona_data['map']['summary_polyline'])    
popup_text = girona_data['name']    
popup_id = str(girona_data['id'])
popup = "<a href=https://www.strava.com/activities/"+popup_id+" target=_blank> "+ popup_text +" </a>"
folium.PolyLine(locations=girona_route, weight=3, color="gold", popup=popup).add_to(fg_challenges)

maui_loop_route = polyline.decode(maui_loop_data['map']['summary_polyline'])    
popup_text = maui_loop_data['name']    
popup_id = str(maui_loop_data['id'])
popup = "<a href=https://www.strava.com/activities/"+popup_id+" target=_blank> "+ popup_text +" </a>"
folium.PolyLine(locations=maui_loop_route, weight=3, color="gold", popup=popup).add_to(fg_challenges)

pt_reyes_s_route = polyline.decode(pt_reyes_s_data['map']['summary_polyline'])    
popup_text = pt_reyes_s_data['name']    
popup_id = str(pt_reyes_s_data['id'])
popup = "<a href=https://www.strava.com/activities/"+popup_id+" target=_blank> "+ popup_text +" </a>"
folium.PolyLine(locations=pt_reyes_s_route, weight=3, color="gold", popup=popup).add_to(fg_challenges)

pt_reyes_b_route = polyline.decode(pt_reyes_b_data['map']['summary_polyline'])    
popup_text = pt_reyes_b_data['name']    
popup_id = str(pt_reyes_b_data['id'])
popup = "<a href=https://www.strava.com/activities/"+popup_id+" target=_blank> "+ popup_text +" </a>"
folium.PolyLine(locations=pt_reyes_b_route, weight=3, color="gold", popup=popup).add_to(fg_challenges)

pt_reyes_r_route = polyline.decode(pt_reyes_r_data['map']['summary_polyline'])    
popup_text = pt_reyes_r_data['name']    
popup_id = str(pt_reyes_r_data['id'])
popup = "<a href=https://www.strava.com/activities/"+popup_id+" target=_blank> "+ popup_text +" </a>"
folium.PolyLine(locations=pt_reyes_r_route, weight=3, color="gold", popup=popup).add_to(fg_challenges)

yosemite_b_route = polyline.decode(yosemite_b_data['map']['summary_polyline'])    
popup_text = yosemite_b_data['name']    
popup_id = str(yosemite_b_data['id'])
popup = "<a href=https://www.strava.com/activities/"+popup_id+" target=_blank> "+ popup_text +" </a>"
folium.PolyLine(locations=yosemite_b_route, weight=3, color="gold", popup=popup).add_to(fg_challenges)

yosemite_r_route = polyline.decode(yosemite_r_data['map']['summary_polyline'])    
popup_text = yosemite_r_data['name']    
popup_id = str(yosemite_r_data['id'])
popup = "<a href=https://www.strava.com/activities/"+popup_id+" target=_blank> "+ popup_text +" </a>"
folium.PolyLine(locations=yosemite_r_route, weight=3, color="gold", popup=popup).add_to(fg_challenges)

bay_1_route = polyline.decode(bay_1_data['map']['summary_polyline'])    
popup_text = bay_1_data['name']    
popup_id = str(bay_1_data['id'])
popup = "<a href=https://www.strava.com/activities/"+popup_id+" target=_blank> "+ popup_text +" </a>"
folium.PolyLine(locations=bay_1_route, weight=3, color="gold", popup=popup).add_to(fg_challenges)

bay_2_route = polyline.decode(bay_2_data['map']['summary_polyline'])    
popup_text = bay_2_data['name']    
popup_id = str(bay_2_data['id'])
popup = "<a href=https://www.strava.com/activities/"+popup_id+" target=_blank> "+ popup_text +" </a>"
folium.PolyLine(locations=bay_2_route, weight=3, color="gold", popup=popup).add_to(fg_challenges)

bay_3_route = polyline.decode(bay_3_data['map']['summary_polyline'])    
popup_text = bay_3_data['name']
popup_id = str(bay_3_data['id'])
popup = "<a href=https://www.strava.com/activities/"+popup_id+" target=_blank> "+ popup_text +" </a>"
folium.PolyLine(locations=bay_3_route, weight=3, color="gold", popup=popup).add_to(fg_challenges)

# add each layer to blank map
fg_challenges.add_to(m)
fg_rides.add_to(m)
fg_runs.add_to(m)  
fg_swims.add_to(m) 

folium.LayerControl().add_to(m)
        
# pushes map to html file where it can be displayed
m.save(r"C:\Users\KevinJ\Strava_Mapping\stravaroutes.html")
