import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
from collections import OrderedDict


#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///hawaii.sqlite', connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

WeatherApp = Flask(__name__)

#################################################
# Flask Routes
#################################################

@WeatherApp.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<startDate><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@WeatherApp.route("/api/v1.0/precipitation")
def precipitationResults():
    """Return of dates and temperature observations from last year"""
    # Query all passengers 
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()
    
    all_prcpData = []
    for dummy in results:  
        precip = {date: prcp for date, prcp in results}
        all_prcpData.append(precip)
    return jsonify(precip)

@WeatherApp.route("/api/v1.0/stations")
def stationsResult():
    return jsonify(session.query(Station.name).all())
    
@WeatherApp.route("/api/v1.0/tobs")
def date_tobs():
   # Query the dates and tobs observations from the last year
   results = session.query(Measurement.date, Measurement.tobs).\
             filter(Measurement.date >= '2016-08-23').all()
   temps = {date: tobs for date, tobs in results}
   #Return the JSON represenation the dictionary
   return jsonify(temps)

@WeatherApp.route("/api/v1.0/<startDate>")
def startResults(startDate):
    Name = ["Min Temp", "Max Temp", "Avg Temp"]
    startResults = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
             filter(Measurement.date >= startDate).all()    
    for row in startResults:
        values = row
    dictionary = dict(zip(Name, values))
    return jsonify(dictionary)

@WeatherApp.route("/api/v1.0/<start>/<end>")
def startEndResults(start, end):
    Name = ["Min Temp", "Max Temp", "Avg Temp"]
    startEndResults = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
    
    for row in startEndResults:
        values = row
    dictionary2 = dict(zip(Name, values))
    return jsonify(dictionary2)

if __name__ == '__main__':
    WeatherApp.run(debug=True)
