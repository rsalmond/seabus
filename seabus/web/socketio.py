from __future__ import absolute_import

import flask_socketio
from seabus.web.web import app

socketio = flask_socketio.SocketIO(app)


@socketio.on('connect', namespace='/seabus_data')
def on_connect():
    pass
