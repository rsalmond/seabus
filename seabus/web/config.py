import os
import seabus

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'

class Dev(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/seabus.db'.format(os.path.abspath(os.path.dirname(seabus.__file__)))
