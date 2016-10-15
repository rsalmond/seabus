from flask import Flask, jsonify
import oboe
from oboeware import OboeMiddleware
from seabus.common.models import Boat, Telemetry, engine
from seabus.common.memcached import mc_client

app = Flask(__name__)
tv_app = OboeMiddleware(app)

@app.route("/data/v1")
def seabus():
    telemetry = {'boats': []}
    for boat in Boat.all_seabuses():
        lat = lon = None

        cached_telemetry = mc_client.get(str(boat.mmsi))

        if not cached_telemetry:
            seabus_telemetry = Telemetry.latest_for_boat(boat)
            lat = seabus_telemetry.lat
            lon = seabus_telemetry.lon
            # cache for next time
            cached_telemetry = {'lat': seabus_telemetry.lat, 'lon': seabus_telemetry.lon}
            mc_client.set(str(boat.mmsi), cached_telemetry)
        else:
            lat = cached_telemetry.get('lat')
            lon = cached_telemetry.get('lon')
            
        if None not in (lat, lon):
            name = boat.name
            id = boat.id
            telemetry['boats'].append(
                {'lat': lat,
                'lon': lon,
                'name': name,
                'id': id
                }
            )

    return jsonify(telemetry)

