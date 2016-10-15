from __future__ import absolute_import
from seabus.web.web import socketio

@socketio.on('connect', namespace='/seabus_data')
def on_connect():
    pass
