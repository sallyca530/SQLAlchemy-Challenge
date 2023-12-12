# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
#Home Page
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to my Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )
#################################################
#Precipation route - 
#Convert the query results from your precipitation analysis
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine) 

    # Find the most recent date in the data set.
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    # Calulate last year
    year = dt.datetime.strptime(last_date.date, '%Y-%m-%d')
    minus_one_year = year - dt.timedelta(days = 365)
    # Perform a query to retrieve the data and precipitation scores
    precip = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date.between(\
    func.strftime('%Y-%m-%d', minus_one_year),
    func.strftime('%Y-%m-%d', year))).all()

    session.close()

    #Return the JSON representation of your dictionary.
    query_precip = []
    for date, prcp in precip:
        p_dict = {}
        p_dict[date] = prcp #date as key and prcp as value
        query_precip.append(p_dict)
    return jsonify(p_dict)
#################################################
#Station route - 
#JSON list of stations
@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)

    # Query station list
    stations_list = session.query(Measurement.station).\
        group_by(Measurement.station).all()
    
    session.close()

    #Return the JSON list.
    stations_all = list(np.ravel(stations_list))
    return jsonify(stations_all)
#################################################
# #Temperature route - 
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    #Query the dates and temperature observations of the 
    # most-active station for the previous year of data.
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date.date
    year = dt.datetime.strptime(last_date.date, '%Y-%m-%d')
    minus_one_year = year - dt.timedelta(days = 365)

    most_active_st_yr = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == "USC00519281", Measurement.date.between(\
        func.strftime('%Y-%m-%d', minus_one_year),
        func.strftime('%Y-%m-%d', year))).all()
    
    session.close()

    #Return a JSON list of temperature observations for the previous year.
    tobs_results = []
    for date, tobs in most_active_st_yr:
        t_dict = {}
        t_dict[date] = tobs
        tobs_results.append(t_dict)
    return jsonify(t_dict)
# #################################################
# #start route -
# @app.route("/api/v1.0/<start>")
# def start(start_date):
#     session = Session(engine)

#     last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

#     #minimum temperature, the average temperature, 
#     # and the maximum temperature for a specified start.
#     start_result = session.query(Measurement.date,func.max(Measurement.tobs),func.avg(Measurement.tobs),func.min(Measurement.tobs)).\
#         filter(Measurement.date.between(\
#                 start_date,
#                 last_date.date)).\
#         group_by(Measurement.date).\
#         order_by(Measurement.date).all()
    
#     session.close()

#     #Return a JSON list
#     start_tobs=[]
#     for date, tmin, tavg, tmax in start_result:
#         tobs_start_dict={}
#         tobs_start_dict["Date"] = date
#         tobs_start_dict["TMIN"] = tmin
#         tobs_start_dict["TAVG"] = tavg
#         tobs_start_dict["TMAX"] = tmax
#         start_tobs.append(tobs_start_dict)
#     return jsonify(start_tobs)  
# #################################################
# #end route -
# @app.route("/api/v1.0/<start>/<end>")
# def end(start_date, last_date):
#     session = Session(engine)

#     last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

#     #minimum temperature, the average temperature, 
#     # and the maximum temperature for a specified start-end range.
#     start_result = session.query(Measurement.date,func.max(Measurement.tobs),func.avg(Measurement.tobs),func.min(Measurement.tobs)).\
#         filter(Measurement.date.between(\
#                 start_date,
#                 last_date.date)).\
#         group_by(Measurement.date).\
#         order_by(Measurement.date).all()
#     session.close()

#     #Return a JSON list
#     start_end_tobs=[]
#     for date, tmin, tavg, tmax in start_result:
#         tobs_start_end_dict = {}
#         tobs_start_end_dict["Date"] = date
#         tobs_start_end_dict["TMIN"] = tmin
#         tobs_start_end_dict["TAVG"] = tavg
#         tobs_start_end_dict["TMAX"] = tmax
#         start_end_tobs.append(tobs_start_end_dict)
#     return jsonify(start_end_tobs)  
# #################################################
# Run the app
if __name__ == "__main__":
    app.run(debug=True)





