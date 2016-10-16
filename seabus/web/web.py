from flask import Flask
import oboe
from oboeware import OboeMiddleware
from seabus.web.blueprint import blueprint
from seabus.common.database import db
from seabus.web.socketio import socketio


def create_app(config):
    app = Flask(__name__)
    app.config.from_object('seabus.web.config.{}'.format(config))
    socketio.init_app(app)
    app.register_blueprint(blueprint)
    db.init_app(app)
    #TODO: tv_app = OboeMiddleware(app)
    return app
