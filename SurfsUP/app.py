# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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

    #list
    stations_list = session.query(Station.station, Station.name).\
        group_by(Station.station).all()

    session.close()

    #Return the JSON representation of your dictionary.
    stations_all = []
    for station in stations_list:
        s_dict = {}
        s_dict["station"] = station
        s_dict["name"] = name
        stations_all.append(s_dict)

    return jsonify(stations_all)



   