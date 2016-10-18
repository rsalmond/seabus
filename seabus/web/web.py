from flask import Flask
import oboe
from oboeware import OboeMiddleware
from seabus.web.blueprint import blueprint
from seabus.common.database import db
from seabus.web.socketio import socketio

def create_app(config=None):
    app = Flask(__name__)

    if config is not None:
        app.config.from_object('seabus.web.config.{}'.format(config))
    else:
        app.config.from_object('seabus.web.config.Dev')

    socketio.init_app(app)
    app.register_blueprint(blueprint)
    db.init_app(app)
    tv_app = OboeMiddleware(app)
    return tv_app
