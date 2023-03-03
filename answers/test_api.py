import pytest
from .app import app
from . import db
from .models import weather, weatherstats


@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()
    with app.app_context():
        weather_data = weather(
            StationID="station_name",
            Dt=11111111,
            MaxTemp=1,
            MinTemp=1,
            PPT=10,
            Year=1111
        )

        stats_data = weatherstats(
            Year=1000,
            StationID="station_name",
            AvgMaxTemp=1,
            AvgMinTemp=1,
            AccPPT=1
        )
        db.session.add(weather_data)
        db.session.add(stats_data)
        db.session.commit()

    yield client


def test_weather_reports(client):
    app.config["TESTING"] = True
    client = app.test_client()
    response = client.get("/weather?date=11111111")
    print(response.json)
    assert response.status_code == 200
    assert response.json == [{"Dt":"11111111","MaxTemp":1,"MinTemp":1,"PPT":10,"StationID":"station_name","Year":"1111"}]

def test_weather_stats(client):
    app.config["TESTING"] = True
    client = app.test_client()
    response = client.get("/weather/stats?year=1000")
    assert response.status_code == 200
    assert response.json == [{"AccPPT":1,"AvgMaxTemp":1.0,"AvgMinTemp":1.0,"StationID":"station_name","Year":"1000"}]