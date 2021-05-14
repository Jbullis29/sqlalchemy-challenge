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
        f'/api/v1.0/stations <br/>'
        f'/api/v1.0/tobs <br/>'
        f'/api/v1.0/<start> <br/>'
        f'/api/v1.0/<start>/<end>'
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

@app.route('/api/v1.0/tobs')
def tobs():
    import datetime as dt
    start_date = dt.datetime(2016,8,18)
    temps = sesh.query(precipitation.station, precipitation.date, precipitation.tobs).\
    filter(precipitation.station == 'USC00519281', precipitation.date >= start_date).all()
    temps_list = [{'station':temp[0], 'date':temp[1], 'temp':temp[2]} for temp in temps]
    return jsonify(temps_list)

@app.route('/api/v1.0/<start>')
def analytics (start):
    
    user_start = sesh.query(func.min(precipitation.date), func.min(precipitation.tobs), 
    func.avg(precipitation.tobs), func.max(precipitation.tobs)).\
        filter(precipitation.date >= start)
    results = {'Start Date': user_start[0][0],  'Minimum recording': user_start[0][1],
    'Maximum Recording': user_start[0][3], 'Average Recording': user_start[0][2]}
    sesh.close()
    return jsonify(results)

@app.route('/api/v1.0/<start>/<end>')
def analytics2 (start,end):
    
    user_start = sesh.query(func.min(precipitation.date),func.max(precipitation.date),
    func.min(precipitation.tobs), func.avg(precipitation.tobs), func.max(precipitation.tobs)).\
        filter(precipitation.date >= start).\
            filter(precipitation.date <= end)
    results = {'Minimum recording': user_start[0][2], 'Maximum Recording': user_start[0][4], 
    'Average Recording': user_start[0][3],'Start Date': user_start[0][0], 
    'End Date': user_start[0][1]}
    sesh.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)