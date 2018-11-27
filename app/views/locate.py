
""" Resources for:

    - recording taxi position (/tracking/taxi)
    - reading taxi position (/tracking/customer)
"""

from app import app, request, API_KEY, API_URI
from app.modules import database
from datetime import datetime
from json import loads
import requests


@app.route('/tracking/mobile/driver', methods=['POST'])
def f_driver():
    """
    Tracks geographical position from the taxi driver's Mobile Device,
    based on coordinates (lat/lon) provided by the Mobile App (through
    the activated GPS circuit).

    Reverse Geocode lookup is perfomed on LocationIQ API.
    """
    if request.method == "POST":
        ts = datetime.now()
        query = {}
        ride_id = request.form.get('ride_id')
        driver_id = request.form.get('driver_id')
        driver_token = request.form.get('driver_token')
        query["lat"] = request.form.get('lat')
        query["lon"] = request.form.get('lon')
        query["key"] = API_KEY
        query["format"] = "json"
        response = requests.get(API_URI, params=query).text
        data = loads(response)
        addr = data.get("address")
        del query["key"]
        del query["format"]
        dbase = database.Database()
        result = dbase.add_location(ride_id, driver_id, driver_token,
                                  addr, query, ts)
        return result

@app.route('/tracking/mobile/passenger', methods=['GET'])
def f_passenger():
    """
    Provides the last tracked geographical position from the taxi drive's
    Mobile Device, for the ride (RideID) which was requested by the passnger.
    """
    if request.method == "GET":
        ride_id = request.args.get('ride_id')
        user_id = request.form.get('user_id')
        user_token = request.form.get('user_token')
        dbase = database.Database()
        result = dbase.read_cur_location(ride_id, user_id, user_token)
        return result
