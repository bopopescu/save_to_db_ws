# -*- coding: utf-8 -*-
import sys
# sys.path.append('./lib')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.measurementDto import *
from datetime import datetime
from sqlalchemy import MetaData

connection = None
session = None
engine = None


def clear_data(engine, metadata, session):
    for table in reversed(metadata.sorted_tables):
        session.execute(table.delete())
        session.commit()
        engine.execute("ALTER TABLE "+table.name+" AUTO_INCREMENT = 1;")
    print 'Clear tables'


def generate_example_data():
    global session
    sensor_type = SensorType(name="Temperature")

    session.add(sensor_type)

    sensor_unit_1 = SensorUnit(name="Celsius", symbol=u'\u2103')
    sensor_unit_2 = SensorUnit(name="Fahrenheit", symbol=u'\u2109')

    session.add(sensor_unit_1)
    session.add(sensor_unit_2)

    sensor = Sensor(sensor_type=sensor_type, sensor_unit=sensor_unit_1, name="Przykładowy sensor", enabled=True)

    session.add(sensor)

    weather_station = WeatherStation(name="Testowa stacja", position_x=222, position_y=444,
                                     address="Sala E0/7", enabled=True, token="token")
    session.add(weather_station)

    session.commit()
    print 'Generate and save example data'


def check_correct_token(ws_id, token):
    global session
    query = session.query(WeatherStation).filter_by(id=ws_id, token=token).count()

    if query != 1:
        return False
    return True


def save_to_database(model):
    from util.DatetimeUtil import string2datetime
    global session

    for measurement in model.measurements:
        if session.query(Sensor).filter_by(id=measurement.sensor_id, enabled=True).count() == 1:
            session_measurement = Measurement(weather_station_id=model.ws_id,
                                              sensor_id=measurement.sensor_id,
                                              value=measurement.value,
                                              created_at=string2datetime(model.time))
            session.add(session_measurement)
        else:
            raise Exception("Sensor id: "+str(measurement.sensor_id)+". Wrong sensor id or actually sensor is disabled")
    session.commit()


def connect_to_database():
    global connection
    global session
    global engine

    engine = create_engine('mysql+mysqlconnector://nkr-projekty:tjp60daoEkVq05P5@orfi.uwm.edu.pl/nkr-projekty')
    connection = engine.connect()

    Session = sessionmaker(bind=engine)
    session = Session()

    metadata = MetaData()
    metadata.reflect(bind=engine)

    # clear_data(engine, metadata, session)
    # generate_example_data()


def disconnect_database():
    global connection
    connection.close()
