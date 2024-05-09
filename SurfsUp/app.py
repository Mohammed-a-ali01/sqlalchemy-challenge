import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Flask Setup
app = Flask(__name__)

# Define routes
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        "<h1>Welcome to the Climate App.</h1>"
        "<h2>These are the available routes:</h2>"
        "<h3>/api/v1.0/precipitation</h3><br/>"
        "<h3>/api/v1.0/stations</h3><br/>"
        "<h3>/api/v1.0/tobs</h3><br/>"
        "<h3>/api/v1.0/YYYY-MM-DD</h3><br/>"
        "<h3>/api/v1.0/YYYY-MM-DD/YYYY-MM-DD</h3>"
    )

@app.route("/api/v1.0/precipitation")

def precipitation():
    """Return JSON representation of precipitation data for the last year."""
    session = Session(engine)
    
    most_recent = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = func.date(most_recent, "-1 year")

    precipitation_data = session.query(Measurement.date, Measurement.prcp) \
        .filter(Measurement.date >= one_year_ago, Measurement.date <= most_recent) \
        .all()

    session.close()

    precip_dict = {date: prcp for date, prcp in precipitation_data}

    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return JSON list of stations."""
    session = Session(engine)
    
    stations = session.query(Station.station).all()
    
    session.close()

    station_list = [station[0] for station in stations]

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return JSON list of temperature observations for the last year."""
    session = Session(engine)

    most_recent = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = func.date(most_recent, "-1 year")

    active_station = session.query(Measurement.station) \
        .group_by(Measurement.station) \
        .order_by(func.count(Measurement.station).desc()) \
        .first()[0]

    temperature_data = session.query(Measurement.date, Measurement.tobs) \
        .filter(Measurement.station == active_station, Measurement.date >= one_year_ago) \
        .all()

    session.close()

    tobs_list = {date: tobs for date, tobs in temperature_data}

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_temperatures(start):
    """Return JSON list of minimum, average, and maximum temperatures from a start date."""
    session = Session(engine)

    temperatures = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)) \
        .filter(Measurement.date >= start) \
        .all()

    session.close()

    temperature_list = [{"Min Temperature": temp[0], "Avg Temperature": temp[1], "Max Temperature": temp[2]} for temp in temperatures]

    return jsonify(temperature_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end_temperatures(start, end):
    """Return JSON list of minimum, average, and maximum temperatures between start and end dates."""
    session = Session(engine)

    temperatures = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)) \
        .filter(Measurement.date >= start, Measurement.date <= end) \
        .all()

    session.close()

    temperature_list = [{"Min Temperature": temp[0], "Avg Temperature": temp[1], "Max Temperature": temp[2]} for temp in temperatures]

    return jsonify(temperature_list)

if __name__ == "__main__":
    app.run(debug=True)
