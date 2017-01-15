from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class PrefixerBase(Base):

    __abstract__ = True

    _the_prefix = 'ws_'

    @declared_attr
    def __tablename__(cls):
        return cls._the_prefix + cls.__incomplete_tablename__


class Log(PrefixerBase):
    __incomplete_tablename__ = 'log'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    created_at = Column(DateTime)

    def __repr__(self):
        return "<Log(content='%s', created_at='%s')>" % (
        self.content, self.created_at)


class SensorUnit(PrefixerBase):
    __incomplete_tablename__ = 'sensor_unit'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    symbol = Column(String)

    def __repr__(self):
        return "<SensorUnit(name='%s', unit='%s')>" % (
        self.name, self.unit)

    sensors = relationship("Sensor", back_populates="sensor_unit")


class SensorType(PrefixerBase):
    __incomplete_tablename__ = 'sensor_type'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<SensorType(name='%s')>" % (
        self.name)

    sensors = relationship("Sensor", back_populates="sensor_type")


class Sensor(PrefixerBase):
    __incomplete_tablename__ = 'sensor'

    id = Column(Integer, primary_key=True)
    sensor_type_id = Column(Integer, ForeignKey(PrefixerBase._the_prefix+'sensor_type.id'))
    sensor_unit_id = Column(Integer, ForeignKey(PrefixerBase._the_prefix+'sensor_unit.id'))
    name = Column(String)
    enabled = Column(Boolean)

    sensor_type = relationship("SensorType", back_populates="sensors")
    sensor_unit = relationship("SensorUnit", back_populates="sensors")

    measurements = relationship("Measurement", back_populates="sensor")

    def __repr__(self):
        return "<Sensor(sensor_type_id='%s', sensor_unit_id='%s', name='%s', enabled='%s')>" % (
        self.sensor_type_id, self.sensor_unit_id, self.name, self.enabled)


class WeatherStation(PrefixerBase):
    __incomplete_tablename__ = 'weather_station'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    position_x = Column(Integer)
    position_y = Column(Integer)
    address = Column(String)
    enabled = Column(Boolean)
    token = Column(String)

    measurements = relationship("Measurement", back_populates="weather_station")

    def __repr__(self):
        return "<WeatherStation(name='%s', position_x='%d', position_y='%d', address='%s', enabled='%s', token='%s')>" % (
            self.name, self.position_x, self.position_y, self.address, self.enabled, self.token)


class Measurement(PrefixerBase):
    __incomplete_tablename__ = 'measurement'

    id = Column(BigInteger, primary_key=True)
    weather_station_id = Column(Integer, ForeignKey(PrefixerBase._the_prefix+'weather_station.id'))
    sensor_id = Column(Integer, ForeignKey(PrefixerBase._the_prefix + 'sensor.id'))
    value = Column(Float)
    created_at = Column(DateTime)

    weather_station = relationship("WeatherStation", back_populates="measurements")
    sensor = relationship("Sensor", back_populates="measurements")

    def __repr__(self):
        return "<Measurement(weather_station_id='%s', sensor_id='%d', value='%d', created_at='%s')>" % (
            self.weather_station_id, self.sensor_id, self.value, self.created_at)
