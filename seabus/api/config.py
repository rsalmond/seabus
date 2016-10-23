import os
import seabus

class Config(object):
    PORT = 6000
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class Test(Config):
    TESTING = True

class Dev(Config):
    DEBUG=True
    seabus_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/db_seabus.db'.format(seabus_project_root)

class Prod(Config):
    DEBUG=False
    seabus_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/db_seabus.db'.format(seabus_project_root)
