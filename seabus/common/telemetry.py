from __future__ import absolute_import

from seabus.common.models import Boat, Telemetry
from seabus.common.memcached import mc_client

def fetch_telemetry():
    """
    retrieve current seabus telemetry
        try memcached first
        fall back to db if not cached, caching for next use
    """
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

    return telemetry
