import os
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker,relationship, backref
from sqlalchemy import create_engine, DateTime, Boolean, Column, Integer, String, ForeignKey

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
    dim_to_starbord = Column(Integer, default=None)
    type_and_cargo = Column(Integer, default=None)

    def __init__(self, mmsi):
        self.mmsi = mmsi
        self.save()

    @classmethod
    def by_mmsi(cls, mmsi):
        return session.query(cls).filter_by(mmsi=mmsi).first()
