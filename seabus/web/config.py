import os
import seabus

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////seabus/data/db_seabus.db'
    LISTENER_HOST = '0.0.0.0'
    LISTENER_PORT = 3000
    LISTENER_UPDATE_URL = 'http://web:5000/update'

class Test(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class Dev(Config):
    DEBUG=True

class Prod(Config):
    pass
