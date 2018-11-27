
from app.modules import database
from app.modules import location
import os
import sys
import time
import unittest

db = database.Database()

class Probe(unittest.TestCase):


    ride_id = "181100001"

    driver = "Robert De Niro"
    driver_username = "deniro"
    driver_password = os.urandom(4).hex()
    driver_token = "3c6cd670b094"

    passenger = "Al Pacino"
    passenger_username = "pacino"
    passenger_password = os.urandom(4).hex()
    passenger_token = "c74767d8d9c2"

    #
    # USA/NY - New York
    #
    #   - from: The Lucerne Hotel
    #   - to: Museum of Natural History
    #
    coordinates = [
                        ("40.783620", "-73.978080"),
                        ("40.784465", "-73.978080"),
                        ("40.784465", "-73.976321"),
                        ("40.783734", "-73.975581"),
                        ("40.783271", "-73.974530"),
                        ("40.782694", "-73.973200"),
                        ("40.781947", "-73.971977")
    ]
    addresses = list()


    def test01_create_user_driver(self):
        """ Creating user (driver). """
        self.assertIsInstance(db.create_user("driver",
                                              Probe.driver,
                                              Probe.driver_username,
                                              Probe.driver_password,
                                              Probe.driver_token), dict)


    def test02_create_user_passenger(self):
        """ Creating user (passenger). """
        self.assertIsInstance(db.create_user("passenger",
                                              Probe.passenger,
                                              Probe.passenger_username,
                                              Probe.passenger_password,
                                              Probe.passenger_token), dict)


    def test03_location_reverse(self):
        """ Getting address for each geographical coordinate. """
        search = location.Location()
        for pos in Probe.coordinates[:]:
            addr = search.reverse(pos[0], pos[1])
            if addr == 1:
                Probe.coordinates.remove(pos)
            else:
                Probe.addresses.append(addr)
        addr_count = [pos for pos in Probe.addresses if type(pos) == dict]
        self.assertNotEqual(len(addr_count), 0)


    def test04_track_position(self):
        """ Tracking address for each geographical coordinate. """
        results = []
        for coord, addr in zip(Probe.coordinates, Probe.addresses):
            result = db.track_position(Probe.ride_id, Probe.driver_username,
                                         addr, coord, Probe.driver_token)
            results.append(result)
            time.sleep(1) # giving a break for LocationIQ API (avoid burst)
        results_count = [addr for addr in results if type(addr) is str]
        self.assertNotEqual(len(results_count), 0)


    def test05_get_last_position(self):
        """ Getting last tracked position, for a specific ride (ride_id). """
        self.assertIsInstance(db.get_last_position(Probe.ride_id,
                                                   Probe.passenger_username,
                                                   Probe.passenger_token), dict)


if __name__ == "__main__":
    unittest.main(failfast=True)
