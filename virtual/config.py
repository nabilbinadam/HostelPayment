import os


class Config:
    # Set your database URI here
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://hostelpayment:abc123@localhost/hostel-payment'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)  # A random secret key for session management

