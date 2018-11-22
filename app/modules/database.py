
from pymongo import MongoClient

class Database():

    def __init__(self):
        """ Configuring MongoDB client. """
        self.client = MongoClient(serverSelectionTimeoutMS=6000)


    def add_location(self, ride_id, taxi_id, location, query, timestamp):
        db = self.client.taxi.RideTracking
        try:
            record_id = db.insert({
                "RideID":ride_id,
                "TaxiID":taxi_id,
                "TrackedAddress":location.get("address"),
                "GeoQuery":query,
                "TrackTime":timestamp
            }
            self.client.close()
            return record_id
        except Exception as e:
            return "Fail to add record to RideTracking: %s" % e

