from . import app
from .models import weather, weatherstats
from .schema import WeatherSchema, WeatherStatSchema
from flask import Flask, request, jsonify
from flasgger import Swagger
swagger = Swagger(app)


weather_schema = WeatherSchema(many=True)
weather_stat_schema = WeatherStatSchema(many=True)

@app.route('/weather', methods=['GET'])
def get_weather():
    """
    This endpoint returns a paginated list of weather data for a given date and station id,
    or for all weather data if no date or station id is specified.
    ---
    parameters:
        - name: page
          in: query
          type: integer
          default: 1
          description: The page number to return.
        - name: per_page
          in: query
          type: integer
          default: 100
          description: The number of results per page.
        - name: date
          in: query
          type: integer
          description: The date for which to return weather data (in YYYYMMDD format).
        - name: stationid
          in: query
          type: string
          description: The station id for which to return weather data.

    responses:
        200:
            description: OK 
    """
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=100, type=int)
    date = request.args.get('date',type=int)
    stationid = request.args.get('stationid')
    if date and stationid:
        all_items = weather.query.filter(weather.Dt==date,weather.StationID==stationid).paginate(page=page, per_page=per_page, error_out=False)
        result = weather_schema.dump(all_items)
        return jsonify(result)
    if date:
        all_items = weather.query.filter(weather.Dt==date).paginate(page=page, per_page=per_page, error_out=False)
        result = weather_schema.dump(all_items)
        return jsonify(result)
    if stationid:
        all_items = weather.query.filter(weather.StationID==stationid).paginate(page=page, per_page=per_page, error_out=False)
        result = weather_schema.dump(all_items)
        return jsonify(result)
    all_items = weather.query.paginate(page=page, per_page=per_page, error_out=False)
    result = weather_schema.dump(all_items)
    return jsonify(result)


@app.route('/weather/stats', methods=['GET'])
def get_stats():
    """
    This endpoint retrieves weather statistics based on the given parameters.
    ---
    parameters:
        - name: page
          in: query
          type: integer
          default: 1
          required: false
          description: The page number to return
        - name: per_page
          in: query
          type: integer
          default: 100
          required: false
          description: The number of items to return per page
        - name: year
          in: query
          type: integer
          required: false
          description: The year to filter by
        - name: stationid
          in: query
          type: string
          description: The station id for which to return weather data.
    responses:
        200:
            description: OK
    """
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=100, type=int)
    year = request.args.get('year',type=int)
    stationid = request.args.get('stationid')
    if year and stationid:
        all_items = weatherstats.query.filter(weatherstats.Year==year,weatherstats.StationID==stationid).paginate(page=page, per_page=per_page, error_out=False)
        result = weather_stat_schema.dump(all_items)
        return jsonify(result)
    if year:
        all_items = weatherstats.query.filter(weatherstats.Year==year).paginate(page=page, per_page=per_page, error_out=False)
        result = weather_stat_schema.dump(all_items)
        return jsonify(result)
    if stationid:
        all_items = weatherstats.query.filter(weatherstats.StationID==stationid).paginate(page=page, per_page=per_page, error_out=False)
        result = weather_stat_schema.dump(all_items)
        return jsonify(result)
    all_items = weatherstats.query.paginate(page=page, per_page=per_page, error_out=False)
    result = weather_stat_schema.dump(all_items)
    return jsonify(result)
