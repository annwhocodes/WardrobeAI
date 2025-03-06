from crewai import Agent, Task, Crew
import requests, os, json
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


class SearchTool:
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")

    def search(self, query):
        """Search for clothing items using SerpAPI."""
        if not self.SERPAPI_KEY:
            raise ValueError("SERPAPI_KEY is missing! Set it as an environment variable.")

        params = {
            "engine": "google_shopping",
            "q": query,
            "hl": "en",
            "gl": "us",
            "api_key": self.SERPAPI_KEY
        }

        try:
            response = requests.get("https://serpapi.com/search", params=params)
            response.raise_for_status()

            data = response.json()
            shopping_results = data.get("shopping_results", [])

            if not shopping_results:
                print(f"No shopping results found for query: {query}.")
                return []

            products = [
                {"name": p.get("title", "N/A"), "price": p.get("price", "N/A"), "url": p.get("product_link", "N/A"), "image": p.get("thumbnail", "N/A")}
                for p in shopping_results[:10]  # Limit to top 10 results
            ]

            return products

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return []
        except json.JSONDecodeError:
            print("Error parsing JSON response. Check API output format.")
            return []


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

        # Use the search tool to find specific items
        search_results = []
        for item in outfit:
            result = search_tool.func(item)
            if result:
                search_results.append({"item": item, "products": result})

        return search_results


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

search_tool = Tool(
    name="Search Clothing",
    func=lambda query: SearchTool().search(query),
    description="Searches for clothing items based on a query using SerpAPI."
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
    tools=[suggest_outfit_tool, search_tool],  # Add the search tool here
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
    expected_output="A list of search results for recommended clothing items based on the weather conditions."
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

    print(f"Recommended outfit for {city}:")
    for item in outfit:
        print(f"\nItem: {item['item']}")
        for product in item["products"]:
            print(f"  - Name: {product['name']}")
            print(f"    Price: {product['price']}")
            print(f"    URL: {product['url']}")
            print(f"    Image: {product['image']}")
            