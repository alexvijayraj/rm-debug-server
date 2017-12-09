from db import db

# model class for users
class UserModel(db.Model):
    __tablename__ = 'users'

    # create all the required columns
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    mobile = db.Column(db.String(50))
    source = db.Column(db.String(50))
    source_uid = db.Column(db.String(50))
    user_type = db.Column(db.String(50))
    rating = db.Column(db.String(50))
    vehicle_uid = db.Column(db.String(50))
    user_status = db.Column(db.String(50))

    def __init__(self, uid, first_name, last_name, email, mobile, source, source_uid, user_type, rating, vehicle_uid, user_status):
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.mobile = mobile
        self.source = source
        self.source_uid = source_uid
        self.user_type = user_type
        self.rating = rating
        self.vehicle_uid = vehicle_uid
        self.user_status = user_status
