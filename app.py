

from flask import Flask, request
import requests
import re


app = Flask(__name__)

key = "API_KEY000000"
uri = "https://us1.locationiq.com/v1/reverse.php"


@app.route('/locate')
def f_index():
    qs = {}
    qs["key"] = key
    qs["lat"] = request.args.get('lat')
    qs["lon"] = request.args.get('lon')
    qs["format"] = "json"
    r = requests.get(uri, params=qs)
    return r.text


if __name__ == "__main__":
    app.run(debug=True)
