# Weather Data Collection Tool

A Python utility for collecting and storing weather forecast data from multiple cities using the OpenWeatherMap API.

## Overview

This tool fetches weather forecast data for specified cities and stores it in a CSV database. It utilizes OpenWeatherMap's Geocoding API to convert city names into geographic coordinates, then retrieves weather data using those coordinates.

## Features

- Geocoding of city names to latitude/longitude coordinates
- Support for multiple cities
- Automatic database updates without duplicates
- Storage in CSV format for easy analysis

## Requirements

- Python 3.6+
- Required Python packages:
  - requests
  - pandas
  - datetime
  - typing

## Setup

1. Clone this repository
2. Install required packages:
   ```
   pip install requests pandas
   ```
3. Create an `output` directory in the project folder

## Usage

1. Open `main.py` and insert your OpenWeatherMap API key:
   ```python
   apikey = 'YOUR_API_KEY_HERE'
   ```

2. Modify the list of cities as needed:
   ```python
   city_names = ['London', 'Dubai', 'Port Louis', 'Paris']
   ```

3. Run the script:
   ```
   python main.py
   ```

4. Weather data will be stored in `output/weatherdb.csv`

## API Reference

### OpenWeatherMap Geocoding API

This project uses the [OpenWeatherMap Geocoding API](https://openweathermap.org/api/geocoding-api) to convert city names to geographic coordinates.

- API Endpoint: `http://api.openweathermap.org/geo/1.0/direct`
- Parameters:
  - `q`: City name
  - `appid`: API key

Example:
```
http://api.openweathermap.org/geo/1.0/direct?q=London&appid=YOUR_API_KEY
```

### OpenWeatherMap Forecast API

This project uses the [OpenWeatherMap Forecast API](https://openweathermap.org/forecast5) to retrieve weather forecasts.

- API Endpoint: `http://api.openweathermap.org/data/2.5/forecast`
- Key Parameters:
  - `lat`, `lon`: Latitude and longitude
  - `appid`: API key
  - `units`: Measurement units (default: 'metric')

Example:
```
http://api.openweathermap.org/data/2.5/forecast?lat=51.5074&lon=-0.1278&appid=YOUR_API_KEY&units=metric
```

## Functions

### `geocoding_weather_location(city_name, apikey)`
Converts a city name to geographic coordinates.

### `fetch_weather_data(latitude, longitude, apikey, units, city, country)`
Fetches weather forecast data for specific coordinates.

### `update_weather_db(city_names, apikey, db)`
Updates an existing weather database with new forecast data.

### `main(apikey, city_names)`
Main function to initialize or update the weather database.

## Output Data

The CSV database includes the following columns:

- Date and Time (UTC)
- Temperature (°C)
- Weather (main category)
- Description (detailed weather description)
- Wind Speed (m/s)
- Humidity (%)
- City
- Country

