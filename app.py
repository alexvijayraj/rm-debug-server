import os

from flask import Flask, request
from flask_restful import Resource, Api

from resources.user import User, GetUser, UpdateUser, DeleteUser
from resources.ride import RequestRide, PostRide, GetRide, UpdateRideStatus, UpdateRideRatings
from resources.vehicle import Vehicle, GetVehicle, UpdateVehicle, DeleteVehicle

# initialize app and db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

# to create all tables and the data.db file if doesn't exist
@app.before_first_request
def create_tables():
    db.create_all()

#User management end points
api.add_resource(User, '/create_user')
api.add_resource(GetUser, '/get_user/<string:uid>')
api.add_resource(UpdateUser, '/update_user')
api.add_resource(DeleteUser, '/delete_user/<string:uid>')

#Vehicle management end points
api.add_resource(Vehicle, '/create_vehicle')
api.add_resource(GetVehicle, '/get_vehicle/<string:uid>')
api.add_resource(UpdateVehicle, '/update_vehicle')
api.add_resource(DeleteVehicle, '/delete_vehicle/<string:uid>')

#Ride management end points
api.add_resource(RequestRide, '/request_ride')
api.add_resource(PostRide, '/post_ride')
api.add_resource(GetRide, '/get_ride/<string:uid>')
api.add_resource(UpdateRideStatus, '/update_ride_status')
api.add_resource(UpdateRideRatings, '/update_ride_ratings')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port = 5000, debug=True)
