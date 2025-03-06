from crewai import Agent, Task, Crew
import requests,os
from dotenv import load_dotenv

load_dotenv()

class Tool:
    def __init__(self, name, func, description):
        self.name = name
        self.func = func
        self.description = description


class WeatherAgent:
    API_KEY = os.getenv("OPENWEATHER_API_KEY")  

    def fetch_weather(self, city):
        """Fetch weather data using OpenWeather API."""
        URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.API_KEY}&units=metric"
        
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
            return {
                "temperature": data["main"]["temp"],
                "condition": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }
        else:
            print("Error fetching weather:", response.text)
            return None

class OutfitSelectionAgent:
    OUTFIT_RECOMMENDATIONS = {
        "hot": ["Cotton T-shirt", "Shorts", "Sunglasses", "Cap"],
        "cold": ["Thermal wear", "Heavy Jacket", "Gloves", "Scarf"],
        "moderate": ["Jeans", "T-shirt", "Light Jacket"],
        "rainy": ["Raincoat", "Waterproof Shoes", "Umbrella"],
        "snowy": ["Winter Jacket", "Boots", "Gloves", "Beanie"],
        "humid": ["Linen Shirt", "Cotton Pants", "Sunglasses"],
        "windy": ["Windbreaker", "Jeans", "Sneakers"]
    }

    def suggest_outfit(self, weather_data):
        """Determines the best outfit based on weather conditions."""
        if not weather_data:
            return "Could not fetch weather data."

        temp = weather_data["temperature"]
        condition = weather_data["condition"].lower()
        humidity = weather_data["humidity"]
        wind_speed = weather_data["wind_speed"]

        outfit = []

        if temp > 25:
            outfit.extend(self.OUTFIT_RECOMMENDATIONS["hot"])
        elif temp < 10:
            outfit.extend(self.OUTFIT_RECOMMENDATIONS["cold"])
        else:
            outfit.extend(self.OUTFIT_RECOMMENDATIONS["moderate"])

        if "rain" in condition:
            outfit.extend(self.OUTFIT_RECOMMENDATIONS["rainy"])
        elif "snow" in condition:
            outfit.extend(self.OUTFIT_RECOMMENDATIONS["snowy"])

        if humidity > 70:
            outfit.extend(self.OUTFIT_RECOMMENDATIONS["humid"])

        if wind_speed > 6:
            outfit.extend(self.OUTFIT_RECOMMENDATIONS["windy"])

        return list(set(outfit))

fetch_weather_tool = Tool(
    name="Fetch Weather",
    func=lambda city: WeatherAgent().fetch_weather(city),
    description="Fetches current weather data for a given city."
)

suggest_outfit_tool = Tool(
    name="Suggest Outfit",
    func=lambda weather: OutfitSelectionAgent().suggest_outfit(weather),
    description="Recommends clothing based on the given weather details."
)

weather_agent = Agent(
    role="Weather Expert",
    goal="Provide real-time weather updates for any city.",
    backstory="A meteorologist trained in understanding weather patterns, predicting changes, and providing actionable insights.",
    tools=[fetch_weather_tool], 
    memory=True
)

outfit_agent = Agent(
    role="Fashion Stylist",
    goal="Suggest the best outfit based on the weather conditions.",
    backstory="A fashion consultant with expertise in weather-based clothing recommendations, ensuring users dress appropriately for any climate.",
    tools=[suggest_outfit_tool], 
    memory=True
)

weather_task = Task(
    description="Get the current temperature, weather conditions, humidity, and wind speed for a city.",
    agent=weather_agent,
    expected_output="A dictionary containing the temperature, weather condition, humidity, and wind speed for the specified city."
)

outfit_task = Task(
    description="Recommend a suitable outfit based on the provided weather details.",
    agent=outfit_agent,
    context=[weather_task], 
    expected_output="A list of recommended clothing items based on the weather conditions."
)

wardrobe_crew = Crew(
    agents=[weather_agent, outfit_agent],
    tasks=[weather_task, outfit_task]
)

if __name__ == "__main__":
    city = input("Enter your city: ")
    
    print("\nFetching weather data...")
    weather_data = fetch_weather_tool.func(city)
    
    print(f"Weather Data for {city}: {weather_data}")

    print("\nSelecting the best outfit...")
    outfit = suggest_outfit_tool.func(weather_data) 

    print(f"Recommended outfit for {city}: {outfit}")   