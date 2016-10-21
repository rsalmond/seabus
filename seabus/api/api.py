from flask import Flask
import oboe
from oboeware import OboeMiddleware
from seabus.api.blueprint import blueprint
from seabus.common.database import db

def create_app(config=None):
    app = Flask(__name__)

    if config is not None:
        app.config.from_object('seabus.api.config.{}'.format(config))
    else:
        app.config.from_object('seabus.api.config.Dev')

    app.register_blueprint(blueprint)
    db.init_app(app)
    app.wsgi_app = OboeMiddleware(app.wsgi_app)
    return app
