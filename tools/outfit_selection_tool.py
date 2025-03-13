from Utils.groq_api import analyze_outfit
from tools.search_tool import search_online_outfits
from Utils.logger import log
from crewai import tool

@tool("Select Outfit")
def select_outfit(weather_data, wardrobe_data, user_preferences):
    """
    Uses Groq LLaMA Vision Model to determine the best outfit.
    If the wardrobe lacks a suitable outfit, searches online for alternatives.
    """
    suggested_outfit = analyze_outfit(weather_data, wardrobe_data, user_preferences)
    
    if suggested_outfit:
        log(f"Suggested outfit from wardrobe: {suggested_outfit}")
        return {"outfit": suggested_outfit, "online_suggestions": None}
    
    log("No suitable outfit found. Searching online...")
    online_suggestions = search_online_outfits(weather_data, user_preferences)
    
    return {"outfit": None, "online_suggestions": online_suggestions}
