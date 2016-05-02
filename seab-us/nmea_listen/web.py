from models import Boat, Telemetry, engine
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/seabus")
def seabus():
    telemetry = {'boats': []}
    for boat in Boat.all():
        if len(boat.telemetry) > 0:
            lat = boat.telemetry[0].lat
            lon = boat.telemetry[0].lon
            name = boat.name
            telemetry['boats'].append(
                {'lat': lat,
                'lon': lon,
                'name': name
                }
            )

    return jsonify(telemetry)

if __name__ == '__main__':
    app.run(debug=True)
