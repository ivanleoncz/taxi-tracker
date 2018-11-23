
""" View for /locate resource. """

from app import app, request, API_KEY, API_URI
from app.modules import database
from datetime import datetime
import requests
import json


@app.route('/locate')
def f_locate():
    """ Performs Reverse Geocode lookup on LocationIQ API. """
    timestamp = datetime.now()
    query = {}
    ride_id = request.args.get('ride_id')
    taxi_id = request.args.get('taxi_id')
    query["lat"] = request.args.get('lat')
    query["lon"] = request.args.get('lon')
    query["key"] = API_KEY
    query["format"] = "json"
    response = requests.get(API_URI, params=query).text
    data = json.loads(response)
    address = data.get("address")
    del query["key"]
    del query["format"]
    dbase = database.Database()
    result = dbase.add_location(ride_id, taxi_id, address, query, timestamp)
    if type(result) is bson.objectid.ObjectId:
        return 0
    else:
        return 1
