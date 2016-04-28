import os
import logging
from datetime import datetime as dt
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker,relationship, backref
from sqlalchemy import create_engine, DateTime, Boolean, Column, Integer, String, ForeignKey

from errors import InvalidBeaconError

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log.addHandler(sh)

engine = create_engine('sqlite:///{}/test.db'.format(os.path.dirname(os.path.realpath(__file__))))
DBSession = sessionmaker(bind=engine)
session = DBSession()
Base = declarative_base()

class ModelBase(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    @classmethod
    def by_id(cls, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def all(cls):
        return session.query(cls).all()

    @classmethod
    def count(cls):
        return session.query(cls).count()

    def save(self):
        session.add(self)
        session.commit()

class Boat(ModelBase):
    __tablename__ = 'boats'
    
    is_seabus = Column(Boolean, default=False)
    mmsi = Column(Integer, nullable=False, unique=True)
    name = Column(String(120), default=None)
    dim_to_bow = Column(Integer, default=None)
    dim_to_stern = Column(Integer, default=None)
    dim_to_port = Column(Integer, default=None)
    dim_to_star = Column(Integer, default=None)
    type_and_cargo = Column(Integer, default=None)
    lastseen_on = Column(DateTime, default = dt.utcnow)

    def __init__(self, mmsi):
        self.mmsi = mmsi
        self.save()

    @classmethod
    def from_beacon(cls, beacon):
        """ return existing boat record if present or create and return
        a new one """
        mmsi = beacon.get('mmsi')
        
        # cant do anything without an mmsi
        if mmsi is None:
            raise InvalidBeaconError

        boat = session.query(cls).filter_by(mmsi=mmsi).first()

        if boat is None:
            boat = Boat(mmsi)
        else:
            # if we've seen this boat before update lastseen time
            boat.lastseen_on = dt.utcnow()

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


class Telemetry(ModelBase):
    __tablename__ = 'telemetry'

    def __init__(self):
        pass
