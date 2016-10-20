import pdb
import unittest
from flask_testing import TestCase
from seabus.nmea_listen.listener import decode
from seabus.common.models import Boat, Telemetry
from seabus.common.database import db
from seabus.web.web import create_app

class TelemetryTest(TestCase):
    """
    Note: 
    boat_msg beacon should decode as:
        {u'destination': u'@@@@@@@@@@@@@@@@@@@@',
        u'dim_d': 5L, 
        u'name': u'BURRARD OTTER II    ', 
        u'eta_hour': 24L, 
        u'ais_version': 1L, 
        u'draught': 0.0, 
        u'mmsi': 316028554L, 
        u'repeat_indicator': 0L, 
        u'dim_b': 17L, 
        u'dim_c': 7L, 
        u'dte': 0L, 
        u'dim_a': 17L, 
        u'eta_day': 0L, 
        u'eta_minute': 60L, 
        u'callsign': u'CFN6722', 
        u'spare': 0L,
        u'eta_month': 0L, 
        u'type_and_cargo': 60L, 
        u'fix_type': 1L, 
        u'id': 5L, 
        u'imo_num': 9688180L}

    pos_msg decodes:
        {u'slot_timeout': 0L, 
        u'sync_state': 0L, 
        u'true_heading': 229L, 
        u'sog': 9.199999809265137, 
        u'rot': 0.0, 
        u'nav_status': 5L, 
        u'repeat_indicator': 0L,
        u'raim': False, 
        u'slot_offset': 2273L,
        u'id': 1L,
        u'spare': 0L, 
        u'cog': 226.60000610351562,
        u'timestamp': 59L, 
        u'y': 49.28786087036133, 
        u'x': -123.1065444946289, 
        u'position_accuracy': 0L, 
        u'rot_over_range': False, 
        u'mmsi': 316028554L, 
        u'special_manoeuvre': 0L}
    """

    boat_msg = '!AIVDM,2,1,1,A,54eHnRT2Cm7@<HsKO;89E9858B0uA@E:0TV2220t28A7540Ht0000000,0*37\r\n!AIVDM,2,2,1,A,000000000000000,2*25'
    pos_msg = '!AIVDM,1,1,,A,14eHnRU01LG<M`:L<vKHnW;n00SQ,0*2D'

    def create_app(self):
        return create_app(config='Test')

    def setUp(self):
        db.create_all()
        boat_beacon = decode(self.boat_msg)
        pos_beacon = decode(self.pos_msg)
    
        boat = Boat.from_beacon(boat_beacon)
        telemetry = Telemetry.from_beacon(pos_beacon)

        assert boat is not None
        assert telemetry is not None

        telemetry.set_boat(boat)
        telemetry.smart_save()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_decode_sanity(self):
        seabus = Boat.all_seabuses()[0]
        assert 'BURRARD' in seabus.name

    def test_cache_storage(self):
        """ test that a telemetry object which goes into memcached is the same as one which comes out """
        seabus = Boat.all_seabuses()[0]
        telemetry = Telemetry.from_db_for_boat(seabus)

        telemetry.put_cache()
        cached_telemetry = Telemetry.from_cache_for_boat(seabus)

        assert telemetry == cached_telemetry

if __name__ == '__main__':
    unittest.main()
