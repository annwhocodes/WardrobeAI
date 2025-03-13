import requests
from Utils.logger import log
import os
from dotenv import load_dotenv
from crewai import tool
load_dotenv()

@tool("Get Current Weather")
def fetch_weather_data(location):
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        weather_data = response.json()
        log(f"Fetched weather data: {weather_data}")
        return weather_data
    else:
        log(f"Error fetching weather data: {response.text}")
        return None
