from flask import Flask
from flask_socketio import SocketIO
import oboe
from oboeware import OboeMiddleware
from seabus.web.blueprint import blueprint

socketio = SocketIO()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object('seabus.web.config.{}'.format(config))
    app.register_blueprint(blueprint)
    db.init_app(app)
    #TODO: tv_app = OboeMiddleware(app)
    socketio.init_app(app)
    return app
