from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class GeoManager:
    def distance(self, lat, lon, lat1, lon1):
        from_place = (lat, lon)
        to_place = (lat1, lon1)
        d = geodesic(from_place, to_place).km
        return d

    def address_to_lat_long(self, address):
        geolocator = Nominatim(user_agent="geo_converter")
        location = geolocator.geocode(address)
        if location:
            latitude = location.latitude
            longitude = location.longitude
            return latitude, longitude
        else:
            return None
