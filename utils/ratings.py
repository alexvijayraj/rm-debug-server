import sqlite3
from db import db
from models.user_model import UserModel

# to add rating to an user
def add_ratings(uuid, new_rating):

    # get rating of that user
    current_rating = get_current_rating(uuid)

    if(current_rating > 0 and current_rating <= 5):
        rating = (new_rating + current_rating)/2
    else:
        rating = new_rating

    # update the newly calculated rating
    update_rating(uuid, rating)


# get the current rating of the current user
def get_current_rating(uuid):
    user = UserModel.query.filter_by(uid=uuid).first()

    if user is None:
        return 99

    return float(user.rating)

# to update the new rating after calculation
def update_rating(uuid, rating):
    user = UserModel.query.filter_by(uid=uuid).first()
    user.rating = rating
    db.session.commit()

# get the new rider rating
def get_rider_rating(ride):

    ride_ratings = ride['ride_ratings']

    return ride_ratings['rider']

# get the new driver rating
def get_driver_rating_new(ride):
    ride_ratings = ride['ride_ratings']

    return ride_ratings['driver']
