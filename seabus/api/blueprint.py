from flask import Blueprint, jsonify
from seabus.web.socketio import socketio
from seabus.common.telemetry import seabus_telemetry

blueprint = Blueprint(__name__, __name__)

@blueprint.route('/data/v1')
def position_data():
    """
    Serve up position data to API clients
    """
    telemetry = seabus_telemetry()
    return jsonify(telemetry)
    
