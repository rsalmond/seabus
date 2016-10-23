from __future__ import absolute_import

from seabus.common.models import Boat, Telemetry
from seabus.common.memcached import mc_client
import oboe

@oboe.log_method('seabus_telemetry')
def seabus_telemetry():
    """
    retrieve current seabus telemetry
    """
    telemetry = {'boats': []}

    for boat in Boat.all_seabuses():
        boat_telemetry = Telemetry.get_for_boat(boat)

        with oboe.profile_block('make_dict'):
            telemetry['boats'].append({
                'lat': boat_telemetry.lat,
                'lon': boat_telemetry.lon,
                'true_heading': boat_telemetry.true_heading,
                'name': boat.name,
                'id': boat.id
            })

    return telemetry
