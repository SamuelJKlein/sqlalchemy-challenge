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
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"/api/v1.0/*insert start date*<br/>"
        f"/api/v1.0/*insert start date*/*insert end date* <br/>"
    )
# Precipitation Route returns precpitation data from the last year recorded in the database
@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_data = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()
    prcp_dict = {}
    for row in prcp_data:
        prcp_dict[row[0]] = row[1]

    return jsonify(prcp_dict)

# Stations route returns JSON list of all stations in the database.
@app.route("/api/v1.0/stations")
def stations():
    station_data = session.query(Measurement.station).group_by(Measurement.station)
    station_list = []
    for row in station_data:
        station_list.append(row[0])
    return jsonify(station_list)

# tobs route returns temp data from the most active station for the last year recorded in the database.
@app.route("/api/v1.0/tobs")
def tobs():
    temp_data = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23').all()
    temp_dict = {}
    for row in temp_data:
        temp_dict[row[0]] = row[1]
    return jsonify(temp_dict)

#start route returns data that was recorded following the date in the url.

@app.route("/api/v1.0/<start_date>")
def start_date(startdate):
    data = session.query(Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).group_by(Measurement.date).filter(Measurement.date >= start_date).all()
    data_dict = {}
    for row in data:
        row_dict = {}
        row_dict['min_temp'] = row[1]
        row_dict['max_temp'] = row[2]
        row_dict['avg_temp'] = row[3]
       
        data_dict[row[0]] = row_dict
    return jsonify(data_dict)
#start end date route returns data that was recorded within the range of dates in the url.
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date(start_date,end_date):
    data = session.query(Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).group_by(Measurement.date).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    data_dict = {}
    for row in data:
        row_dict = {}
        row_dict['min_temp'] = row[1]
        row_dict['max_temp'] = row[2]
        row_dict['avg_temp'] = row[3]
       
        data_dict[row[0]] = row_dict
    return jsonify(data_dict)

if __name__ == "__main__":
    app.run(debug=False)
    
    