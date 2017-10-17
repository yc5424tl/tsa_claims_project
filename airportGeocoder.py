import requests
google_maps_api_key = aizasyab7fmjhvphsbrid5ythmzkkuvsrs9k4qc

airportGeocodes = {}

buildAirportGeocodes(){
  
  airports = foo_airports_df.index
  for airport in airports:
    url='https://maps.googleapis.com/maps/api/geocode/json?address={}&amp;key={}'.format(airport + ' airport', google_maps_api_key)
    r = requests.get(url).json()
    
    lat = r['results'][0]['geometry']['location']['lat']
    lng = r['results'][0]['geometry']['location']['lng']
    
    airportGeocodes.append(airport:[lat, lng]) #should include airport code here
