from models import Boat, Telemetry, engine
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/data/v1")
def seabus():
    telemetry = {'boats': []}
    for boat in Boat.all():
        lat = lon = None
        if boat.is_seabus:
            seabus_telemetry = Telemetry.latest_for_boat(boat)
            if seabus_telemetry is None:
                continue
            lat = seabus_telemetry.lat
            lon = seabus_telemetry.lon
        else:
            if len(boat.telemetry) > 0:
                lat = boat.telemetry[0].lat
                lon = boat.telemetry[0].lon
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

if __name__ == '__main__':
    app.run(debug=True)
