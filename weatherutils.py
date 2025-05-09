import requests
import pandas as pd
from datetime import datetime
from typing import Optional, Tuple, List

def geocoding_weather_location(city_name: str, apikey: str) -> Optional[Tuple[float, float, str, str]]:
    """
    Retrieves the latitude and longitude for a given city name using the OpenWeatherMap Geocoding API.

    Parameters:
    city_name (str): The name of the city.
    apikey (str): API key for OpenWeatherMap.

    Returns:
    tuple: A tuple containing latitude, longitude, city name, and country if successful. 
           Returns None if there's an error.
    """
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={apikey}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data:
            item = data[0]
            return item['lat'], item['lon'], item['name'], item['country']
        else:
            print(f"No data found for city: {city_name}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def fetch_weather_data(latitude: float, longitude: float, apikey: str, units: str = 'metric',
    city: Optional[str] = None, country: Optional[str] = None) -> Optional[pd.DataFrame]:
    """
    Fetches weather data from OpenWeatherMap API for given coordinates.

    Parameters:
    latitude (float): Latitude of the location.
    longitude (float): Longitude of the location.
    apikey (str): API key for OpenWeatherMap.
    units (str): Units of measurement ('metric' or 'imperial'). Default is 'metric'.
    city (str): Name of the city.
    country (str): Name of the country.

    Returns:
    pandas.DataFrame: A DataFrame containing weather data if successful. 
                      Returns None if there's an error.
    """
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={apikey}&units={units}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        weather_data = data['list']
        df = pd.DataFrame({
            'Date and Time': [pd.to_datetime(item['dt_txt']).tz_localize('UTC') for item in weather_data],
            'Temperature (°C)': [item['main']['temp'] for item in weather_data],
            'Weather': [item['weather'][0]['main'] for item in weather_data],
            'Description': [item['weather'][0]['description'] for item in weather_data],
            'Wind Speed (m/s)': [item['wind']['speed'] for item in weather_data],
            'Humidity (%)': [item['main']['humidity'] for item in weather_data],
            'City': city,
            'Country': country
        })
        return df
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def update_weather_db(city_names: List[str], apikey: str, db: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """
    Updates or creates a weather database with current weather data for given cities.

    Parameters:
    city_names (list of str): List of city names to fetch weather data for.
    apikey (str): API key for OpenWeatherMap.
    db (pandas.DataFrame): Existing weather data DataFrame. If None, a new DataFrame is created.

    Returns:
    pandas.DataFrame: Updated or newly created DataFrame with weather data.
    """
    if db is None:
        db = pd.DataFrame()

    for city_name in city_names:
        geo_data = geocoding_weather_location(city_name, apikey)
        if geo_data:
            latitude, longitude, city, country = geo_data
            df_updates = fetch_weather_data(latitude, longitude, apikey, city=city, country=country)
            if df_updates is not None:
                db = pd.concat([db, df_updates])
                db = db.drop_duplicates(['Date and Time', 'City', 'Country'])

    if not db.empty:
        db = db.sort_values(by=['Date and Time', 'City'], ascending=[True, True]).reset_index(drop=True)
        latestTimeStamp = db['Date and Time'].max()
        nowTimeStamp = datetime.utcnow()
        print(f'Weather Database updated at {nowTimeStamp} UTC. Including updates till {latestTimeStamp} UTC')

    return db


def main(apikey: str, city_names: List[str]) -> pd.DataFrame:
    """
    Main function to initialize or update the global weather database.

    Parameters:
    apikey (str): API key for OpenWeatherMap.
    city_names (list of str): List of city names to fetch weather data for.

    Returns:
    pandas.DataFrame: DataFrame containing the updated weather data.
    """
    global db
    if 'db' not in globals():
        db = pd.DataFrame()

    db = update_weather_db(city_names, apikey, db)
    return db
