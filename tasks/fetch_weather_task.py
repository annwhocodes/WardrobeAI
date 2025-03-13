from agents.weather_agent import WeatherAgent
from crewai import Task
import logging

class FetchWeatherTask:
    def __init__(self, agent=None):
        if agent is None:
            # Create the weather agent if not provided
            agent = WeatherAgent().create_agent()

        self.task = Task(
            name="FetchWeatherTask",
            description="Fetch current weather data for New York City.",
            agent=agent,
            expected_output="Weather data including temperature, humidity, and conditions.",
            output_key="weather_data",
            async_execution=False,  # Try both True and False
        )