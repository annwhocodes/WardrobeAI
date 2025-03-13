import requests
from Utils.logger import log
from crewai import tool
@tool("Search Online Outfits")
def search_online_outfits(weather_data, user_preferences):
    """
    Searches online fashion websites for outfit recommendations based on weather and preferences.
    Returns top 10 outfit suggestions with purchase links.
    """
    query = f"{weather_data['main']['temp']}°C {user_preferences.get('style', 'casual')} outfit"
    url = f"https://serpapi.com/search?q={query}&num=10&api_key=your_serpapi_key"

    response = requests.get(url)
    
    if response.status_code == 200:
        results = response.json().get("items", [])
        outfits = [{"name": item["title"], "link": item["link"]} for item in results[:10]]
        log(f"Found {len(outfits)} outfit recommendations online")
        return outfits
    
    log("Failed to fetch online outfits")
    return []
