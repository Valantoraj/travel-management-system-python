import requests
from geopy.distance import geodesic
import json


class HotelFinder:
    def __init__(self):
        self.overpass_url = "http://overpass-api.de/api/interpreter"
    def distance(self, lat, lon, lat1, lon1):
        from_place = (lat, lon)
        to_place = (lat1, lon1)
        d = geodesic(from_place, to_place).km
        return d
    
    def find_nearest_hotels(self, radius, latitude, longitude):
        location_point = (latitude, longitude)  # Latitude, Longitude
        overpass_query = """
    [out:json];
    node["tourism"="hotel"](around:{},{},{});
    out;
""".format(radius, location_point[0], location_point[1])


        response = requests.get(self.overpass_url, params={'data': overpass_query})
        data = response.json()
        max_dist = 0
        hotels = {}
        count = 0

        for element in data['elements']:
            if 'tags' in element and 'name' in element['tags']:
                name = element['tags']['name']
                if not self.is_unwanted(name):
                    latitude = element['lat']
                    longitude = element['lon']
                    dist = self.distance(location_point[0], location_point[1], latitude, longitude)
                    max_dist = max(max_dist, dist)
                    hotels[name.title()] = dist
                    count += 1
                    if count >= 4:
                        break

        if data['elements']:
            if hotels:
                return 1, max_dist, hotels
            else:
                return 2, None, None
        else:
            return 2, None, None

    def is_unwanted(self, name):
        list_unwanted = ['hostels', 'Hostels', 'Hostel', 'Tiffen', 'Lunch', 'Quarters', 'PG', "Cafe", 'cafe', 'Veg',
                         'VEG', 'veg', 'Non Veg', 'non veg', 'Vilas', 'Dhaba', "Dhabha", "Daba", 'dhaba',
                         'restaurant', 'Restaurant', 'உணவகம்']
        return any(unwanted in name for unwanted in list_unwanted)