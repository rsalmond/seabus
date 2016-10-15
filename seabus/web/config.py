import os
import seabus

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'

class Dev(Config):
    DEBUG=True
    seabus_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/seabus.db'.format(seabus_project_root)
