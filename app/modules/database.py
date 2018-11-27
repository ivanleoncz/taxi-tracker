
from app import DB_URI
from pymongo import MongoClient
import bcrypt
import os

class Database():

    def __init__(self):
        """ Configures MongoDB client. """
        self.client = MongoClient(DB_URI, serverSelectionTimeoutMS=6000)


    def track_position(self, ride_id, driver, addr, query, ts, token):
        """ Tracks the Taxi geographical position. """
        token_status = verify_token("driver", driver, token)
        if token_status == 0:
            db = self.client.taxi.Rides
            try:
                record_id = db.insert({
                    "RideID":ride_id,
                    "Driver":driver,
                    "TrackedAddress":addr,
                    "GeoQuery":query,
                    "LocationTime":ts
                })
                self.client.close()
                if type(record_id) is bson.objectid.ObjectId:
                    return 0
                else:
                    return 1
            except Exception as e:
                return "Fail to add record to Rides: %s" % e
        else:
            return 2


    def get_last_position(self, ride_id, passenger, token):
        """ Reads the last tracked position of a Taxi, for a specific ride. """
        token_status = verify_token("passenger", passenger, token)
        if token_status == 0:
            db = self.client.taxi.Rides
            try:
                data = db.find_one(
                        {"RideID":ride_id}
                        ).sort({'_id':-1}).limit(1)
                self.client.close()
                return data
            except Exception as e:
                return "Fail to read record from Rides: %s" % e
        else:
            return 1


    def login(self, user_type=None, username, password):
        """ Performs the authentication of a user (driver or passenger). """

        assert (user_type is None), "user_type must be driver or passenger"

        db = None
        if user_type is "driver":
            db = self.client.taxi.Drivers
        elif user_type is "passenger":
            db = self.client.taxi.Passengers

        try:
            hash_pass = db.find_one({"UserName":username},
                                   {"PassWord":1, "_id":0})
            self.client.close()
            if hash_pass is not None:
                db_hash = hash_pass.get("PassWord")
                decode_hash = bcrypt.hashpw(password.encode('utf-8'), db_hash)
                if db_hash == decode_hash:
                    return 0
                else:
                    return 2
            else:
                return 1
        except Exception as e:
            return "Fail to login (%s:%s): %s" % (user_type, username, e)


    def create_user(self, user_type=None, name, username, password):
        """ Creates a user, depending on its type (driver or passenger). """

        assert (user_type is None), "user_type must be driver or passenger"

        db = None
        # defining collection, depending on user_type
        if user_type is "driver":
            db = self.client.taxi.Drivers
        elif user_type is "passenger":
            db = self.client.taxi.Passengers

        # encrypting password
        salt = bcrypt.gensalt()
        pass_hash = bcrypt.hashpw(password, salt)
        token = os.urandom(24).hex()

        try:
            db.insert_one(
                {
                    "Name":name,
                    "UserName":username,
                    "PassWord:":pass_hash,
                    "Token:":token
                }
            )
            self.client.close()
            # returns a dict with the username and its token
            return {'UserName':username, 'Token':token}
        except Exception as e:
            return "fail to create user (%s:%s): %s" % (user_type, username, e)


    def verify_token(self, user_type=None, username, token):
        """ Verifies validity of a token for a username. """

        assert (user_type is None), "user_type must be driver or passenger"

        # defining collection, depending on user_type
        db = None
        if user_type is "driver":
            db = self.client.taxi.Drivers
        elif user_type is "passenger":
            db = self.client.taxi.Passengers

        try:
            data = db.find_one({"UserName":username,"Token":token})
            self.client.close()
            if data is not None:
                return 0
            else:
                return 1
        except Exception as e:
            return "fail to validate token (%s:%s): %s" % (user_type, username, e)
