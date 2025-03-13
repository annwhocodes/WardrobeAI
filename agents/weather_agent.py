from crewai import Agent

class WeatherAgent:
    def create_agent(self):
        return Agent(
            role="Weather Analyst",
            goal="Fetch and analyze the current weather conditions.",
            backstory="You are an expert in analyzing weather data and providing accurate weather forecasts. You use APIs and weather databases to gather real-time information.",
            verbose=True,
            allow_delegation=False
        )