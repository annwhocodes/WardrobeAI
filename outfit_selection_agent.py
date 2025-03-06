import requests , os
from dotenv import load_dotenv


load_dotenv()


OUTFIT_RECOMMENDATIONS = {
    "hot": ["Cotton T-shirt", "Shorts", "Sunglasses", "Cap"],
    "cold": ["Thermal wear", "Heavy Jacket", "Gloves", "Scarf"],
    "moderate": ["Jeans", "T-shirt", "Light Jacket"],
    "rainy": ["Raincoat", "Waterproof Shoes", "Umbrella"],
    "snowy": ["Winter Jacket", "Boots", "Gloves", "Beanie"],
    "humid": ["Linen Shirt", "Cotton Pants", "Sunglasses"],
    "windy": ["Windbreaker", "Jeans", "Sneakers"]
}

def get_weather(city):
    """Fetches real-time weather data."""
    API_KEY = os.getenv("OPENWEATHER_API_KEY")  
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

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
        print("Error fetching weather data:", response.text)
        return None

def select_outfit(weather_data):
    """Determines the best outfit based on multiple weather parameters."""
    if not weather_data:
        return "Could not fetch weather data."

    temp = weather_data["temperature"]
    condition = weather_data["condition"].lower()
    humidity = weather_data["humidity"]
    wind_speed = weather_data["wind_speed"]

    outfit = []

    # Temperature-based recommendations
    if temp > 25:
        outfit.extend(OUTFIT_RECOMMENDATIONS["hot"])
    elif temp < 10:
        outfit.extend(OUTFIT_RECOMMENDATIONS["cold"])
    else:
        outfit.extend(OUTFIT_RECOMMENDATIONS["moderate"])

    # Condition-based recommendations
    if "rain" in condition:
        outfit.extend(OUTFIT_RECOMMENDATIONS["rainy"])
    elif "snow" in condition:
        outfit.extend(OUTFIT_RECOMMENDATIONS["snowy"])

    # Humidity considerations
    if humidity > 70:
        outfit.extend(OUTFIT_RECOMMENDATIONS["humid"])

    # Wind speed considerations
    if wind_speed > 6:  # Strong wind
        outfit.extend(OUTFIT_RECOMMENDATIONS["windy"])

    return list(set(outfit))  

if __name__ == "__main__":
    city = input("Enter your city: ")
    weather_data = get_weather(city)
    
    print(f"Weather in {city}: {weather_data}")
    
    outfit = select_outfit(weather_data)
    print(f"Recommended outfit for {city}: {outfit}")
