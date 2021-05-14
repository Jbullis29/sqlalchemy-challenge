#import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
#create engine
engine = create_engine("sqlite:///Data/hawaii.sqlite")
#create base
Base = automap_base()
#connect base to engine
Base.prepare(engine, reflect = True)
#connect base to my individual tables. I knew table name from Jupyter discovery 
precipitation = Base.classes.measurement
station = Base.classes.station

#create a session
sesh = Session(engine)

#Defining app as flask name
app=Flask(__name__)

#First route to main paige
@app.route('/')
def home():
   #returning a bunch of print statements listing my api paths
    return(
        f"The following routes are available: <br/>"
        f'/api/v1.0/precipitation <br/>'
        f'/api/v1.0/stations <br/>'
        f'/api/v1.0/tobs <br/>'
        f'/api/v1.0/<start> <br/>'
        f'/api/v1.0/<start>/<end>'
        )
#First route to return precipitation data
@app.route("/api/v1.0/precipitation")
def mesurments():
    #import DateTime function to help filter data
    import datetime as dt
    start_date = dt.datetime(2016, 8, 23)
    #query to retun data after a certain start date
    results = sesh.query(precipitation.date, precipitation.prcp).\
    filter(precipitation.date >= start_date).all()
    prcp = [{'date': result[0], 'precipitation': result[1]} for result in results]
    #closing my sesion
    sesh.close()
    #Return a json of my tuple
    return jsonify(prcp)

#Second Api to return stations
@app.route("/api/v1.0/stations")
def stations():
    # query to return station names
    station_name = sesh.query(station.station)
    #storing stations in list 
    station_list = [{'station_id':station[0]} for station in station_name]
    # closed session
    sesh.close()
    #jsonify my list
    return jsonify(station_list)
#Next route to return temps 
@app.route('/api/v1.0/tobs')
def tobs():
    #used the DateTime function again
    import datetime as dt
    #define start date
    start_date = dt.datetime(2016,8,18)
    #quried to get station,date and temps filtering by most active
    temps = sesh.query(precipitation.station, precipitation.date, precipitation.tobs).\
    filter(precipitation.station == 'USC00519281', precipitation.date >= start_date).all()
    #storing my data to a list calle Temps_list
    temps_list = [{'station':temp[0], 'date':temp[1], 'temp':temp[2]} for temp in temps]
    #retuned list as Json
    return jsonify(temps_list)

# made new route where users type in a date to the url after /  
@app.route('/api/v1.0/<start>')
def analytics (start):
    #created a query to return desired funtions
    #filter by start which is defined in the fucntion and is connected to values in url
    user_start = sesh.query(func.min(precipitation.date), func.min(precipitation.tobs), 
    func.avg(precipitation.tobs), func.max(precipitation.tobs)).\
        filter(precipitation.date >= start)
    #storing my results by unpacking list and returning labeled values
    results = {'Start Date': user_start[0][0],  'Minimum recording': user_start[0][1],
    'Maximum Recording': user_start[0][3], 'Average Recording': user_start[0][2]}
    #close sesh
    sesh.close()
    #return JSonified list
    return jsonify(results)

#new route for users to search a start and end in url 
@app.route('/api/v1.0/<start>/<end>')
def analytics2 (start,end):
    #Query to return desired values
    #filtered by start which is defined in function
    #also filtered by end whch is defined in the function
    user_start = sesh.query(func.min(precipitation.date),func.max(precipitation.date),
    func.min(precipitation.tobs), func.avg(precipitation.tobs), func.max(precipitation.tobs)).\
        filter(precipitation.date >= start).\
            filter(precipitation.date <= end)
    #stored results in my list 
    results = {'Minimum recording': user_start[0][2], 'Maximum Recording': user_start[0][4], 
    'Average Recording': user_start[0][3],'Start Date': user_start[0][0], 
    'End Date': user_start[0][1]}
    #close sesh
    sesh.close()
    #return json list
    return jsonify(results)
#Always used this if statement to be safe 
if __name__ == '__main__':
    app.run(debug=True)