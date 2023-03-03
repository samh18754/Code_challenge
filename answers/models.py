from . import app,db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Float, Integer
from datetime import datetime
from .ingestor import IngestData, WeatherResult

class weather(db.Model):
    __tablename__ = 'Weather'
    Dt = Column(String, primary_key=True)
    MaxTemp = Column(Float)
    MinTemp = Column(Float)
    PPT = Column(Float)
    StationID = Column(String, primary_key=True)
    Year = Column(Integer)

    def __init__(self, Dt, MaxTemp, MinTemp, PPT, StationID, Year):
        self.Dt = Dt
        self.MaxTemp = MaxTemp
        self.MinTemp = MinTemp
        self.PPT = PPT
        self.StationID = StationID
        self.Year = Year


class weatherstats(db.Model):
    __tablename__ = 'weatherstats'
    Year = Column(Integer, primary_key=True)
    StationID = Column(String, primary_key=True)
    AvgMaxTemp = Column(Float)
    AvgMinTemp = Column(Float)
    AccPPT = Column(Integer)

    def __init__(self, Year, StationID, AvgMaxTemp, AvgMinTemp, AccPPT):
        self.Year = Year
        self.StationID = StationID
        self.AvgMaxTemp = AvgMaxTemp
        self.AvgMinTemp = AvgMinTemp
        self.AccPPT = AccPPT

with app.app_context():       
    db.create_all()

    print(f"Ingestion started at {datetime.now()}")
    data = IngestData("./wx_data")
    result = WeatherResult(data)
    data.to_sql('Weather', con=db.engine, if_exists='replace', index=False)
    result.to_sql('weatherstats', con=db.engine, if_exists='replace', index=False)
    print(f"Ingestion finished at {datetime.now()}")