import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Data/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect = True)

precipitation = Base.classes.measurement

station = Base.classes.station

sesh = Session(engine)


app=Flask(__name__)

@app.route('/')
def home():
    print("Server recieved request for 'Home' page...")
    return(
        f"The following routes are available: <br/>"
        f'/api/v1.0/precipitation <br/>'
        f'/api/v1.0/stations'
        )

@app.route("/api/v1.0/precipitation")
def mesurments():
    
    import datetime as dt
    start_date = dt.datetime(2016, 8, 23)

    results = sesh.query(precipitation.date, precipitation.prcp).\
    filter(precipitation.date >= start_date).all()
    prcp = [{'date': result[0], 'precipitation': result[1]} for result in results]
    sesh.close()
    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stations():
    station_name = sesh.query(station.station)
    station_list = [{'station_id':station[0]} for station in station_name]
    sesh.close()
    return jsonify(station_list)


if __name__ == '__main__':
    app.run(debug=True)