from db import db

# model class for vehicles
class VehicleModel(db.Model):
    __tablename__ = 'vehicles'

    # create all the required columns
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50))
    user_uid = db.Column(db.String(50))
    vehicle_type = db.Column(db.String(50))
    seats = db.Column(db.String())
    reg_number = db.Column(db.String(50))
    fare = db.Column(db.String(50))
    vehicle_status = db.Column(db.String(50))

    def __init__(self, uid, user_uid, vehicle_type, seats, reg_number, fare, vehicle_status):
        self.uid = uid
        self.user_uid = user_uid
        self.vehicle_type = vehicle_type
        self.seats = seats
        self.reg_number = reg_number
        self.fare = fare
        self.vehicle_status = vehicle_status
