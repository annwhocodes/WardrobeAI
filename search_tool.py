import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

if not SERPAPI_KEY:
    raise ValueError("SERPAPI_KEY is missing! Set it as an environment variable.")

print("SERPAPI_KEY:", SERPAPI_KEY)  # Ensure the key is loaded correctly

query = "shirt"

params = {
    "engine": "google_shopping",
    "q": query,
    "hl": "en",
    "gl": "us",
    "api_key": SERPAPI_KEY
}

print("Sending request to SerpAPI...")

try:
    response = requests.get("https://serpapi.com/search", params=params)
    response.raise_for_status()

    # Debugging: Print API response details
    print("API Request URL:", response.url)  # Check the full URL being requested
    print("API Response Status Code:", response.status_code)  # Check if the request succeeded
    print("API Response Content:", response.text)  # Inspect the raw response

    data = response.json()

    print("\nFull API Response:\n", json.dumps(data, indent=2))

    shopping_results = data.get("shopping_results", [])

    if not shopping_results:
        print("No shopping results found. Check if the query is valid or if SerpAPI has data.")

    products = [
        {"url": p.get("product_link", "N/A"), "image": p.get("thumbnail", "N/A")}
        for p in shopping_results[:10]
    ]

    if not products:
        print("No products extracted. Verify API response structure.")
    else:
        print(f"Found {len(products)} products. Saving to products.json.")

    with open("products.json", "w") as file:
        json.dump(products, file, indent=4)

    print("Products successfully saved to products.json")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")

except json.JSONDecodeError:
    print("Error parsing JSON response. Check API output format.")