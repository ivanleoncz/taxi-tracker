#!/bin/bash

# 
# NOTICE: run this script, after running tests.py
#

RIDE_ID="181100001"

DRIVER_URI="http://127.0.0.1:5000/tracking/mobile/driver"
DRIVER_USERNAME="deniro"
DRIVER_TOKEN="3c6cd670b094"
LAT="40.781947"
LON="-73.971977"

PASSENGER_URI="http://127.0.0.1:5000/tracking/mobile/passenger"
PASSENGER_USERNAME="pacino"
PASSENGER_TOKEN="c74767d8d9c2"


# taxi (mobile app) sending geographical coordinates, along with its id and token
echo -e "\nTAXI: sending location"
curl -d username=$DRIVER_USERNAME -d token=$DRIVER_TOKEN -d ride_id=$RIDE_ID -d lat=$LAT -d lon=$LON "$DRIVER_URI"

# passenger (mobile app) polling API for last tracked address
echo -e "\nPASSENGER: getting last tracked address"
curl "$PASSENGER_URI?username=$PASSENGER_USERNAME&token=$PASSENGER_TOKEN&ride_id=$RIDE_ID"
