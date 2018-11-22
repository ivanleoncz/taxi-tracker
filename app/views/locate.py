
""" View for /locate resource. """

from app import app, request, API_KEY, API_URI

import requests


@app.route('/locate')
def f_locate():
    """ Performs Reverse Geocode lookup. """
    qs = {}
    qs["key"] = API_KEY
    qs["lat"] = request.args.get('lat')
    qs["lon"] = request.args.get('lon')
    qs["format"] = "json"
    r = requests.get(API_URI, params=qs)
    return r.text
