import os
import seabus

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class Test(Config):
    TESTING = True

class Dev(Config):
    DEBUG=True
    seabus_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/db_seabus.db'.format(seabus_project_root)
    LISTENER_HOST = '0.0.0.0'
    LISTENER_PORT = 3001
    LISTENER_UPDATE_URL = 'http://dev.seab.us/update'

class Prod(Config):
    DEBUG=True
    seabus_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/db_seabus.db'.format(seabus_project_root)
    LISTENER_HOST = '10.8.0.1'
    LISTENER_PORT = 3000
    LISTENER_UPDATE_URL = 'http://seab.us/update'
