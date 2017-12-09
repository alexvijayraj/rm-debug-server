from app import app
from db import db

db.init_app(app)

# to create all tables and the data.db file if doesn't exist
@app.before_first_request
def create_tables():
    db.create_all()
