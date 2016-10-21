from __future__ import absolute_import

import os
import logging
import pickle
from datetime import datetime as dt

from seabus.common.database import db
from seabus.common.memcached import mc_client
from seabus.common.errors import InvalidBeaconError

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log.addHandler(sh)

def safe_get_type(some_dict, some_key, some_type):
   if some_key in some_dict:
        val = some_dict.get(some_key)
        try:
            val = some_type(val)
        except Exception as e:
            return

        return val

class ModelBase(db.Model):
    """ provide some useful common functions for db models """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __eq__(self, other):
        """ compare class type and (non sqlalchemy) columns for equality """
        if not isinstance(other, self.__class__):
            return False

        for k, v in self.__dict__.iteritems():
            if not k.startswith('_'):
                if getattr(self, k) != getattr(other, k):
                    return False

        return True

    @classmethod
    def by_id(cls, id):
        return db.session.query(cls).filter_by(id=id).first()

    @classmethod
    def all(cls):
        return db.session.query(cls).all()

    @classmethod
    def count(cls):
        return db.session.query(cls).count()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def _mc_key(self):
        """ memcached key based on class name + instance id """
        assert self.id is not None
        return '{}_{}'.format(str(self.__class__.__name__), self.id)

    def put_cache(self):
        """ write this model to memcached """
        mc_client.set(self._mc_key(), pickle.dumps(self))

    @classmethod
    def get_cache(cls, id):
        key = '{}_{}'.format(cls.__name__, id)
        cached = mc_client.get(key)
        if cached is not None:
            return pickle.loads(cached)

class Boat(ModelBase):
    """
    Everetying related to the boat metadata coming in via http://catb.org/gpsd/AIVDM.html#_type_5_static_and_voyage_related_data
    """
    __tablename__ = 'boats'
    
    telemetry = db.relationship('Telemetry', backref='boat')
    is_seabus = db.Column(db.Boolean, default=False)
    mmsi = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(120), default=None)
    dim_to_bow = db.Column(db.Integer, default=None)
    dim_to_stern = db.Column(db.Integer, default=None)
    dim_to_port = db.Column(db.Integer, default=None)
    dim_to_star = db.Column(db.Integer, default=None)
    type_and_cargo = db.Column(db.Integer, default=None)
    lastseen_on = db.Column(db.DateTime, default = dt.utcnow)

    # hard coded from observing data
    seabus_mmsis = [316028554, 316014621, 316011651, 316011649]

    def __init__(self, mmsi):
        self.mmsi = mmsi
        self.save()

    @classmethod
    def all_seabuses(cls):
        boats = []
        for mmsi in Boat.seabus_mmsis:
            # first try to fetch from cache
            boat = Boat.from_cache_by_mmsi(mmsi)
            if boat is not None:
                boats.append(boat)
            else:
                # fall back to db and cache response
                boat = db.session.query(cls).filter_by(mmsi=mmsi).first()
                if boat is not None:
                    boat.put_cache()
                    boats.append(boat)

        if len(boats) > 0:
            return boats

    @classmethod
    def from_beacon(cls, beacon):
        """ return existing boat record if present or create and return
        a new one """

        if beacon.get('id') == 4:
            # msg type 4 is a base station, not a boat
            return 

        mmsi = beacon.get('mmsi')
        
        # cant do anything without an mmsi
        if mmsi is None:
            raise InvalidBeaconError

        boat = db.session.query(cls).filter_by(mmsi=mmsi).first()

        if boat is None:
            boat = Boat(mmsi)
        else:
            # if we've seen this boat before update lastseen time
            boat.lastseen_on = dt.utcnow()

        if boat.mmsi in Boat.seabus_mmsis:
            boat.is_seabus = True

        boat._parse_beacon(beacon)
        boat.save()
        return boat

    def _parse_beacon(self, beacon):
        
        name = beacon.get('name')
        if isinstance(name, basestring):
            self.name = name.strip()

        type_and_cargo = beacon.get('type_and_cargo')

        if type_and_cargo is not None:
            try:
                type_and_cargo = int(type_and_cargo)
                self.type_and_cargo = type_and_cargo
            except Exception as e:
                log.exception(e)
                log.info('Bogus type/cargo in beacon {}'.format(beacon))

        d2bow = beacon.get('dim_a')
        d2stern = beacon.get('dim_b')
        d2port = beacon.get('dim_c')
        d2star = beacon.get('dim_d')

        dimensions = (d2bow, d2stern, d2port, d2star)
        
        if None not in dimensions:
            try:
                dimensions = filter(int, (d2bow, d2stern, d2port, d2star))
            except Exception as e:
                log.info('Bogus dimensions in beacon: {}'.format(beacon))
                
            if len(dimensions) == 4:
                self.dim_to_bow = int(d2bow)
                self.dim_to_stern = int(d2stern)
                self.dim_to_port = int(d2port)
                self.dim_to_star = int(d2star)

    def _mc_key(self):
        """ memcached key based on class name + mmsi """
        assert self.mmsi is not None
        return '{}_{}'.format(str(self.__class__.__name__), self.mmsi)

    @classmethod
    def from_cache_by_mmsi(cls, mmsi):
        key = '{}_{}'.format(cls.__name__, mmsi)
        cached = mc_client.get(key)
        if cached is not None:
            return pickle.loads(cached)
        


class Telemetry(ModelBase):
    """
    Everything related to position, heading, etc coming in via http://catb.org/gpsd/AIVDM.html#_types_1_2_and_3_position_report_class_a
    """
    __tablename__ = 'telemetry'

    boat_id = db.Column(db.Integer, db.ForeignKey('boats.id'))
    nav_status = db.Column(db.Integer)
    pos_accuracy = db.Column(db.Integer)
    lon = db.Column(db.Float)
    lat = db.Column(db.Float)
    speed_over_ground = db.Column(db.Float)
    course_over_ground = db.Column(db.Float)
    true_heading = db.Column(db.Integer)
    rate_of_turn = db.Column(db.Float)
    rate_of_turn_over_range = db.Column(db.Boolean)
    timestamp = db.Column(db.Integer)
    received = db.Column(db.DateTime, default=dt.utcnow)

    def __init__(self):
        pass

    def __repr__(self):
        return '<% {}, {} %>'.format(self.lat, self.lon)

    @classmethod
    def from_beacon(cls, beacon):
        telemetry = Telemetry()
        telemetry._parse_beacon(beacon)
        if telemetry.is_valid():
            return telemetry

    def is_valid(self):
        if None in (self.lat, self.lon):
            return False

        if (self.lat < 0) or (self.lat > 90):
            return False

        if (self.lon < -180) or (self.lon > 180):
            return False

        return True

    def _parse_beacon(self, beacon):
        self.nav_status = safe_get_type(beacon, 'nav_status', int)
        self.pos_accuracy = safe_get_type(beacon, 'position_accuracy', int)
        self.lon = safe_get_type(beacon, 'x', float)
        self.lat = safe_get_type(beacon, 'y', float)
        self.speed_over_ground = safe_get_type(beacon, 'sog', float)
        self.course_over_ground = safe_get_type(beacon, 'cog', float)
        self.true_heading = safe_get_type(beacon, 'true_heading', int)
        self.rate_of_turn = safe_get_type(beacon, 'rot', float)
        self.rate_of_turn_over_range = safe_get_type(beacon, 'rot_over_range',bool)
        self.timestamp = safe_get_type(beacon, 'timestamp', int)

    @classmethod
    def from_db_for_boat(cls, boat):
        return db.session.query(cls).filter_by(boat_id=boat.id).order_by(cls.id.desc()).first()

    def set_boat(self, boat):
        self.boat_id = boat.id

    def smart_save(self):
        """
        Save all telemetry for Seabuses, only latest telemetry for everyone else
        """
        if Boat.by_id(self.boat_id).is_seabus:
            # record every piece of telemetry for each seabus
            if self.is_valid():
                self.save()
        else:
            # drop all previous telemetry for this boat
            if self.is_valid():
                db.session.query(Telemetry).filter_by(boat_id=self.boat_id).delete()
                self.save()

    def _mc_key(self):
        """ key based on class name + boat id should keep memcache pretty clear of junk """
        assert self.boat_id is not None
        return '{}_{}'.format(str(self.__class__.__name__), self.boat_id)

    @classmethod
    def from_cache_for_boat(cls, boat):
        key = '{}_{}'.format(cls.__name__, boat.id)
        cached = mc_client.get(key)
        if cached is not None:
            return pickle.loads(cached)

    @classmethod
    def get_for_boat(cls, boat):
        """ try to fetch the latest telemetry from cache first, if not grab from db and cache for next time """
        telemetry = Telemetry.from_cache_for_boat(boat)
        if not telemetry:
            telemetry = Telemetry.from_db_for_boat(boat)
            telemetry.put_cache()

        return telemetry
