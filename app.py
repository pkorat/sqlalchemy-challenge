import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/temperature<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    prev_date = dt.datetime(2017, 8, 23) - dt.timedelta(days = 365)

    prec_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_date).all()

    session.close()

    perc_dic = {date:perc for date, perc in prec_data}

    return jsonify(perc_dic)


@app.route("/api/v1.0/stations")
def stations():

    stations = session.query(Station.station).all()

    session.close()

    stations = list(np.ravel(stations))

    return jsonify(stations)

@app.route("/api/v1.0/temperature")
def temperature():

    prev_date = dt.datetime(2017, 8, 23) - dt.timedelta(days = 365)

    temp_data = session.query(Measurement.tobs).filter(Measurement.date >= prev_date).\
        filter(Measurement.station == 'USC00519281').all()

    session.close()

    temp_data = list(np.ravel(temp_data))

    return jsonify(temp_data)


if __name__ == '__main__':
    app.run(debug=True)
