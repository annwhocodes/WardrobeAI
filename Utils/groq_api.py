import requests
from Utils.logger import log
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY =os.getenv("GROQ_API_KEY")

def analyze_outfit(weather_data, wardrobe_data, user_preferences):
    """
    Uses Groq LLaMA Vision Model to analyze wardrobe items and select the best outfit.
    """
    url = "https://api.groq.com/v1/analyze_outfit" 

    # Define the payload
    payload = {
        "weather": weather_data,
        "wardrobe": wardrobe_data,
        "preferences": user_preferences
    }

    # Define headers with the API key
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # Make the POST request to the Groq API
        response = requests.post(url, json=payload, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            log(f"Groq model suggested: {result['outfit']}")
            return result["outfit"]
        else:
            log(f"Groq API request failed with status code: {response.status_code}")
            log(f"Response: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        log(f"An error occurred while making the request to Groq API: {e}")
        return None