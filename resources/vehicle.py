from flask import Flask, request
from flask_restful import Resource, Api
from models.user_model import UserModel
from models.vehicle_model import VehicleModel
from db import db
from utils.uuid_generator import get_uuid
from utils.validity import *
import sqlite3

class Vehicle(Resource):
    def post(self):
        data = request.get_json()
        uuid = get_uuid()
        vehicle = { 'uid': uuid,
                 'user_uid': data['user_uid'],
                 'vehicle_type' : data['vehicle_type'],
                 'seats' : data['seats'],
                 'reg_number' : data['reg_number'],
                 'fare' : data['fare'],
                 'vehicle_status' : data['vehicle_status']
               }

        # check if the received values are valid
        if not is_vehicle_valid(vehicle):

            # return the invalid reason
            return {'message': why_invalid(vehicle)}, 400

        vehicle_1 = VehicleModel(uuid, data['user_uid'], data['vehicle_type'], data['seats'], data['reg_number'], data['fare'], data['vehicle_status'])
        db.session.add(vehicle_1)

        user = UserModel.query.filter_by(uid=data['user_uid']).first()
        user.vehicle_uid = uuid

        db.session.commit()

        return {'status': 'success','uid': uuid}, 201

class GetVehicle(Resource):
    def get(self, uid):
        vehicle = VehicleModel.query.filter_by(uid=uid).first()

        if vehicle:
            return {'vehicle': {'uid': vehicle.uid,
                 'user_uid' : vehicle.user_uid,
                 'vehicle_type' : vehicle.vehicle_type,
                 'seats' : vehicle.seats,
                 'reg_number' : vehicle.reg_number,
                 'fare' : vehicle.fare,
                 'vehicle_status' : vehicle.vehicle_status
               }}, 200
        return {'vehicle' : 'null'}, 404

class UpdateVehicle(Resource):
    def put(self):
        data = request.get_json()

        # check if the received values are valid
        if not is_vehicle_valid(data):

            # return the invalid reason
            return {'message': why_invalid(data)}, 400

        vehicle = VehicleModel.query.filter_by(uid=data['uid']).first()

        if vehicle:
            vehicle.uid = data['uid']
            vehicle.user_uid = data['user_uid']
            vehicle.vehicle_type = data['vehicle_type']
            vehicle.seats = data['seats']
            vehicle.reg_number = data['reg_number']
            vehicle.fare = data['fare']
            vehicle.vehicle_status = data['vehicle_status']

            db.session.commit()

            return {'status': 'success','uid': data['uid']}, 201

        # return the invalid reason
        return {'message': 'Invalid vehicle UID'}, 400

class DeleteVehicle(Resource):
    def delete(self, uid):

        vehicle = VehicleModel.query.filter_by(uid=uid).first()

        if vehicle:
            db.session.delete(vehicle)
            db.session.commit()
            return {'message': 'Vehicle deleted'}, 201
        else:
            return {'message': 'Vehicle Not Found'}, 400

# to check of the vehicle is valid or not
def is_vehicle_valid(vehicle):

    # get individual values
    user_uid = vehicle['user_uid']
    vehicle_type = vehicle['vehicle_type']
    seats = vehicle['seats']
    reg_number = vehicle['reg_number']
    fare = vehicle['fare']
    vehicle_status = vehicle['vehicle_status']

    if is_valid_user(user_uid) and is_valid_vehicle_type(vehicle_type) and is_valid_reg_number(reg_number) and is_valid_seats(seats) and is_valid_fare(fare) and is_valid_vehicle_status(vehicle_status):
        return True

    return False

# return the reason for vehicle invalidity
def why_invalid(vehicle):

    # get individual values
    user_uid = vehicle['user_uid']
    vehicle_type = vehicle['vehicle_type']
    seats = vehicle['seats']
    reg_number = vehicle['reg_number']
    fare = vehicle['fare']
    vehicle_status= vehicle['vehicle_status']

    # check for user validity
    if not is_valid_user(user_uid):
        return 'invalid user'

    # check for vehicle type validity
    if not is_valid_vehicle_type(vehicle_type):
        return 'invalid vehicle type. Should be either of ‘BIKE’, ‘HATCHBACK’, ‘SEDAN’, ‘SUV’ and ‘PREMIUM’'

    # check for reg number validity
    if not is_valid_reg_number(reg_number):
        return 'invalid Reg number'

    # check for seats validity
    if not is_valid_seats(seats):
        return 'invalid seats. Should be between 1 and 12'

    # check for fare validity
    if not is_valid_fare(fare):
        return 'invalid fare. Should be between 4 and 100'

    # check for vehicle_type validity
    if not is_valid_vehicle_status(vehicle_status):
        return 'invalid vehicle type. Should be either of AVAILABLE, UNAVAILABLE or BUSY'
