from __future__ import absolute_import
from flask_socketio import SocketIO, emit
from seabus.common.telemetry import fetch_telemetry

socketio = SocketIO()

@socketio.on('connect', namespace='/seabus_data')
def on_connect():
    """
    send initial telemetry on client connect
    """
    telemetry = fetch_telemetry()
    emit('seabus_moved', telemetry)
