
""" Global variables for Taxi Tracker configuration. """

API_KEY="your api key to LocationIQ services"
API_URI = "https://us1.locationiq.com/v1/reverse.php"
DB_USER="mongo"
DB_PASS="mongo"
DB_ADDR="127.0.0.1"
DB_PORT="27017"
DB_URI="mongodb://{0}:{1}@{2}:{3}".format(DB_USER, DB_PASS, DB_ADDR, DB_PORT)
