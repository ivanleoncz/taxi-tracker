
from app import API_URI, API_KEY
from json import loads
import requests

class Location():

    def reverse(self, latitude, longitude):
        """ Performs reverse geocoding, based on geographical coordinates. """
        query = {}
        query["lat"] = latitude
        query["lon"] = longitude
        query["key"] = API_KEY
        query["format"] = "json"
        response = requests.get(API_URI, params=query).text
        data = loads(response)
        addr = data.get("address")
        if type(addr) is dict:
            return addr
        else:
            return 1
