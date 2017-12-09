from db import db

# model class for rides
class RideModel(db.Model):
    __tablename__ = 'rides'

    # create all the required columns
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50))
    driver_uid = db.Column(db.String(50))
    rider_uid = db.Column(db.String(50))
    ride_location = db.Column(db.String())
    ride_time = db.Column(db.String(50))
    ride_cost = db.Column(db.String(50))
    ride_ratings = db.Column(db.String(50))
    vehicle_uid = db.Column(db.String(50))
    ride_status = db.Column(db.String(50))

    def __init__(self, uid, driver_uid, rider_uid, ride_location, ride_time, ride_cost, ride_ratings, vehicle_uid, ride_status):
        self.uid = uid
        self.driver_uid = driver_uid
        self.rider_uid = rider_uid
        self.ride_location = ride_location
        self.ride_time = ride_time
        self.ride_cost = ride_cost
        self.ride_ratings = ride_ratings
        self.vehicle_uid = vehicle_uid
        self.ride_status = ride_status
