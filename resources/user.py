from flask import Flask, request
from flask_restful import Resource, Api
from db import db
from models.user_model import UserModel
from utils.uuid_generator import get_uuid
from utils.ratings import *
from utils.validity import *
import sqlite3

class User(Resource):
    def post(self):
        data = request.get_json()
        uuid = get_uuid()
        user = { 'uid': uuid,
                 'first_name' : data['first_name'],
                 'last_name' : data['last_name'],
                 'email' : data['email'],
                 'mobile' : data['mobile'],
                 'source' : data['source'],
                 'source_uid' : data['source_uid'],
                 'user_type' : data['user_type'],
                 'rating' : '0.0',
                 'user_status': data['user_status']
               }

        # check if the received values are valid
        if not is_user_valid(user):

            # return the invalid reason
            return {'message': why_invalid(user)}, 400

        user_1 = UserModel(uuid, data['first_name'], data['last_name'], data['email'], data['mobile'], data['source'], data['source_uid'], data['user_type'], '0.0', '', data['user_status'])

        db.session.add(user_1)
        db.session.commit()

        return {'status': 'success','uid': uuid}, 201

class GetUser(Resource):
    def get(self, uid):

        user = UserModel.query.filter_by(uid=uid).first()

        if user:
            return {'user': {'uid': user.uid,
                 'first_name' : user.first_name,
                 'last_name' : user.last_name,
                 'email' : user.email,
                 'mobile' : user.mobile,
                 'source' : user.source,
                 'source_uid' : user.source_uid,
                 'user_type' : user.user_type,
                 'rating' : user.rating,
                 'vehicle_uid' : user.vehicle_uid,
                 'user_status' : user.user_status
               }}, 200
        return {'user' : 'null'}, 404

class UpdateUser(Resource):
    def put(self):
        data = request.get_json()

        # check if the received values are valid
        if not is_user_valid(data):

            # return the invalid reason
            return {'message': why_invalid(data)}, 400

        user = UserModel.query.filter_by(uid=data['uid']).first()

        if user:
            user.uid = data['uid']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            user.mobile = data['mobile']
            user.source = data['source']
            user.source_uid = data['source_uid']
            user.user_type = data['user_type']
            user.rating = data['rating']
            user.vehicle_uid = data['vehicle_uid']
            user.user_status = data['user_status']

            db.session.commit()
            return {'status': 'success','uid': user.uid}, 201

        # return the invalid reason
        return {'message': 'Invalid user UID'}, 400

class DeleteUser(Resource):
    def delete(self, uid):

        user = UserModel.query.filter_by(uid=uid).first()

        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted'}, 201
        else:
            return {'message': 'User Not Found'}, 400

# to check if the user is valid or not
def is_user_valid(user):

    # get individual values
    last_name = user['last_name']
    mobile = user['mobile']
    user_type = user['user_type']
    user_status = user['user_status']

    if is_valid_last_name(last_name) and is_valid_mobile(mobile) and is_valid_user_type(user_type) and is_valid_user_status(user_status):
        return True

    return False

# return the reason for user invalidity
def why_invalid(user):

    # get individual values
    last_name = user['last_name']
    mobile = user['mobile']
    user_type = user['user_type']
    user_status = user['user_status']

    # check for last name validity
    if not is_valid_last_name(last_name):
        return 'invalid last name'

    # check for mobile number validity
    if not is_valid_mobile(mobile):
        return 'invalid mobile number'

    # check for user type validity
    if not is_valid_user_type(user_type):
        return 'invalid user type, Should be either DRIVER or RIDER'

    # check for user status validity
    if not is_valid_user_status(user_status):
        return 'invalid user type, Should be either AVAILABLE or UNAVAILABLE or BUSY'
