# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()


# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end> <br/>"
    )
# Precipitation Route returns precpitation data from the last year recorded in the database
@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_data = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= '2016-08-23').all()
    prcp_dict = {}
    for row in prcp_data:
        prcp_dict[row[0]] = row[1]

    return jsonify(prcp_dict)

# Stations route returns JSON list of all stations in the database.
@app.route("/api/v1.0/stations")
def stations():
    station_list = session.query(Measurement.station).group_by(Measurement.station)

    return jsonify(station_list)

# tobs route returns temp data from the most active station for the last year recorded in the database.
@app.route("/api/v1.0/tobs")
def tobs():
    temp_data = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23').all()

    return jsonify(temp_data)

#start route returns all data from the most active station that follows the date in the url.
@app.route("/api/v1.0/<start>")
def start_date(starting_at):
    data = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= starting_at).filter(Measurement.station == "USC00519281").all()

    return jsonify(data)
#start end date route returns all data from the most active station that is within the range of dates in the url.
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(starting_at,ending_at):
    data = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= starting_at).filter(Measurement.date <= ending_at).filter(Measurement.station == "USC00519281").all()

    return jsonify(data)