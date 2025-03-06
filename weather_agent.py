import os
import requests
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

class WeatherAgent:
    def __init__(self):
        self.agent = Agent(
            role="Weather Data Analyst",
            goal="Fetch current weather details for a given location.",
            backstory="An AI-powered meteorologist that provides weather updates.",
            verbose=True
        )

    def get_weather(self, location: str):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_info = {
                "temperature": data["main"]["temp"],
                "condition": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }
            return weather_info
        else:
            return {"error": "Could not fetch weather data."}

if __name__ == "__main__":
    weather_agent = WeatherAgent()
    location = input("Enter your location : ")
    weather_data = weather_agent.get_weather(location)
    print(f"Weather in {location}: {weather_data}")
