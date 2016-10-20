from flask import Blueprint
from seabus.web.socketio import socketio
from seabus.common.telemetry import seabus_telemetry

blueprint = Blueprint(__name__, __name__)

@blueprint.route('/update')
def update():
    """
    called by the nmea listener process when seabus coordinates have been updated
    """
    telemetry = seabus_telemetry()
    socketio.emit('seabus_moved', telemetry, namespace='/seabus_data')
    return ('', 202)
    
