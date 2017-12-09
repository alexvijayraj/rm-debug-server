import sqlite3
from db import db
from models.user_model import UserModel
from models.vehicle_model import VehicleModel

# check if the uuid is of a valid user
def is_valid_user(uuid):

    user = UserModel.query.filter_by(uid=uuid).first()

    if user:
        return True

    return False

## USER validity

# check if the last name is valid
def is_valid_last_name(last_name):

    if isinstance(last_name, str):
        if last_name:
            return True
        else:
            return False
    else:
        return False

# check if the mobile number is valid
def is_valid_mobile(mobile):
    return True

# check if the user type is valid
def is_valid_user_type(user_type):

    list_user_type = ['DRIVER', 'RIDER']

    if user_type in list_user_type:
        return True
    else:
        return False

# check if the user status is valid
def is_valid_user_status(user_status):

    list_user_status = ['AVAILABLE', 'UNAVAILABLE', 'BUSY']

    if user_status in list_user_status:
        return True
    else:
        return False

## RIDE validity

# check if the driver uid is valid
def is_valid_driver_uid(driver_uid):
    return is_valid_user(driver_uid)

# check if the rider uid is valid
def is_valid_rider_uid(rider_uid):
    return is_valid_user(rider_uid)

# check if the ride location is valid
def is_valid_ride_location(ride_location):
    return True

# check if the ride time is valid
def is_valid_ride_time(ride_time):
    return True

# check if the ride cost is valid
def is_valid_ride_cost(ride_cost):

    if isinstance(ride_cost, int):
        return True

    return False

# check if the ride rating is valid
def is_valid_ride_ratings(ride_ratings):
    return True

# check if the vehicle uid is valid
def is_valid_vehicle_uid(vehicle_uid):
     vehicle = VehicleModel.query.filter_by(uid=vehicle_uid).first()

     if vehicle:
         return True
     return False

# check if the ride status is valid
def is_valid_ride_status(ride_status):

    list_ride_status = ['SCHEDULED', 'IN PROGRESS', 'COMPLETED', 'CANCELLED BY RIDER', 'CANCELLED BY DRIVER' ]

    if ride_status in list_ride_status:
        return True
    else:
        return False

## VEHICLE validity

# check if the vehicle type is of a known type
def is_valid_vehicle_type(vehicle_type):

    list_vehicle_type = ['BIKE', 'HATCHBACK', 'SEDAN', 'SUV', 'PREMIUM' ]

    if vehicle_type in list_vehicle_type:
        return True
    else:
        return False

# check if the reg number is valid
def is_valid_reg_number(reg_number):

    return True

# check if the seats is a valid number
def is_valid_seats(seats):

    if (isinstance(seats, int)) and (seats > 0) and (seats < 13):
        return True
    else:
        return False

#check if the fare is a valid number
def is_valid_fare(fare):

    if (isinstance(fare, int)) and (fare > 3) and (fare < 101):
        return True
    else:
        return False

# check for vehicle_status validity
def is_valid_vehicle_status(vehicle_status):

    list_vehicle_status = ['AVAILABLE', 'UNAVAILABLE', 'BUSY' ]

    if vehicle_status in list_vehicle_status:
        return True
    else:
        return False
