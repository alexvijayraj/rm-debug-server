from flask import Flask, request
from flask_restful import Resource, Api
from models.ride_model import RideModel
from db import db
from utils.uuid_generator import get_uuid
from utils.ratings import *
from utils.validity import *
import sqlite3

class RequestRide(Resource):
    def post(self):
        data = request.get_json()
        uuid = get_uuid()
        ride = { 'uid': uuid,
                 'driver_uid': data['driver_uid'],
                 'rider_uid': data['rider_uid'],
                 'ride_location' : data['ride_location'],
                 'ride_time' : data['ride_time'],
                 'ride_cost' : data['ride_cost'],
                 'ride_ratings' : data['ride_ratings'],
                 'vehicle_uid' : data['vehicle_uid'],
                 'ride_status' : data['ride_status']
               }

        # check if the received values are valid
        if not is_ride_valid(ride):

            # return the invalid reason
            return {'message': why_invalid(ride)}, 400

        ride_1 = RideModel(uuid, data['driver_uid'], data['rider_uid'], str(data['ride_location']), str(data['ride_time']), data['ride_cost'], str(data['ride_ratings']), data['vehicle_uid'], data['ride_status'])

        db.session.add(ride_1)
        db.session.commit()

        return {'status': 'success','uid': uuid}, 201

class PostRide(Resource):
    def post(self):
        data = request.get_json()
        uuid = get_uuid()
        ride = { 'uid': uuid,
                 'driver_uid': data['driver_uid'],
                 'rider_uid': data['rider_uid'],
                 'ride_location' : data['ride_location'],
                 'ride_time' : data['ride_time'],
                 'ride_cost' : data['ride_cost'],
                 'ride_ratings' : data['ride_ratings'],
                 'vehicle_uid' : data['vehicle_uid'],
                 'ride_status' : data['ride_status']
               }
        rides.append(ride)

        # check if the received values are valid
        if not is_ride_valid(ride):

            # return the invalid reason
            return {'message': why_invalid(ride)}, 400

        ride_1 = RideModel(uuid, data['driver_uid'], data['rider_uid'], str(data['ride_location']), str(data['ride_time']), data['ride_cost'], str(data['ride_ratings']), data['vehicle_uid'], data['ride_status'])

        db.session.add(ride_1)
        db.session.commit()

        return {'status': 'success','uid': uuid}, 201

class GetRide(Resource):
    def get(self, uid):
        ride = RideModel.query.filter_by(uid=uid).first()

        if ride:
            return {'user': {'uid': ride.uid,
                 'driver_uid' : ride.driver_uid,
                 'rider_uid' : ride.rider_uid,
                 'ride_location' : ride.ride_location,
                 'ride_time' : ride.ride_time,
                 'ride_cost' : ride.ride_cost,
                 'ride_ratings' : ride.ride_ratings,
                 'vehicle_uid' : ride.vehicle_uid,
                 'ride_status' : ride.ride_status
               }}, 200
        return {'ride' : 'null'}, 404

class UpdateRideStatus(Resource):
    def put(self):
        data = request.get_json()

        # check if the received values are valid
        if not is_ride_valid(data):

            # return the invalid reason
            return {'message': why_invalid(data)}, 400

        ride = RideModel.query.filter_by(uid=data['uid']).first()

        if ride:
            ride.ride_status = data['ride_status']
            db.session.commit()

            return {'status': 'success','uid': data['uid']}, 201
        # return the invalid reason
        return {'message': 'Invalid ride UID'}, 400

class UpdateRideRatings(Resource):
    def put(self):
        data = request.get_json()

        ride = RideModel.query.filter_by(uid=data['uid']).first()

        if ride:
            ride.ride_ratings = str(data['ride_ratings'])
            db.session.commit()

        # get the driver uid
        driver_uid = data['driver_uid']

        # get the rider uid
        rider_uid = data['rider_uid']

        # get the new driver rating
        driver_rating_new = get_driver_rating_new(data)

        # get the new rider rating
        rider_rating_new = get_rider_rating(data)

        # update the ratings of the driver and the rider
        add_ratings(rider_uid, rider_rating_new)
        add_ratings(driver_uid, driver_rating_new)

        return {'status': 'success','uid': data['uid']}, 201

# to check if the ride is valid or not
def is_ride_valid(ride):

    # get individual values
    driver_uid = ride['driver_uid']
    rider_uid = ride['rider_uid']
    ride_location = ride['ride_location']
    ride_time = ride['ride_time']
    ride_cost = ride['ride_cost']
    ride_ratings = ride['ride_ratings']
    vehicle_uid = ride['vehicle_uid']
    ride_status = ride['ride_status']

    if is_valid_driver_uid(driver_uid) and is_valid_rider_uid(rider_uid) and is_valid_ride_location(ride_location) and is_valid_ride_time(ride_time) and is_valid_ride_cost(ride_cost) and is_valid_ride_ratings(ride_ratings) and is_valid_vehicle_uid(vehicle_uid) and is_valid_ride_status(ride_status):
        return True

    return False

# return the reason for ride invalidity
def why_invalid(ride):

    # get individual values
    driver_uid = ride['driver_uid']
    rider_uid = ride['rider_uid']
    ride_location = ride['ride_location']
    ride_time = ride['ride_time']
    ride_cost = ride['ride_cost']
    ride_ratings = ride['ride_ratings']
    vehicle_uid = ride['vehicle_uid']
    ride_status = ride['ride_status']

    # check for driver uid validity
    if not is_valid_driver_uid(driver_uid):
        return 'invalid DRIVER'

    # check for rider uid validity
    if not is_valid_rider_uid(rider_uid):
        return 'invalid RIDER'

    # check for ride location validity
    if not is_valid_ride_location(ride_location):
        return 'invalid ride location'

    # check for ride time validity
    if not is_valid_ride_time(ride_time):
        return 'invalid ride time'

    # check for ride cost validity
    if not is_valid_ride_cost(ride_cost):
        return 'invalid ride cost'

    # check for ride ratings validity
    if not is_valid_ride_ratings(ride_ratings):
        return 'invalid ride ratings'

    # check for vehicle uid validity
    if not is_valid_vehicle_uid(vehicle_uid):
        return 'invalid vehicle uid'

    # check for ride status validity
    if not is_valid_ride_status(ride_status):
        return 'invalid ride status. Should be one of SCHEDULED, IN PROGRESS, COMPLETED, CANCELLED BY RIDER, CANCELLED BY DRIVER'
