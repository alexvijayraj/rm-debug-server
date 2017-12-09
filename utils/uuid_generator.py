import uuid

# method to return a new UUID in string format
def get_uuid():

    # generate new uuid in string format
    new_uuid = str(uuid.uuid4())

    return new_uuid
