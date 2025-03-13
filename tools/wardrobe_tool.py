from Utils.firebase_utils import fetch_user_wardrobe
from Utils.logger import log
from crewai import tool

@tool("Check Wardrobe Availability")
def check_wardrobe_availability(user_id, outfit):
    wardrobe_items = fetch_user_wardrobe(user_id)
    available = any(outfit.lower() in item.lower() for item in wardrobe_items)
    
    log(f"Checking wardrobe for {user_id}: {outfit} -> {'Available' if available else 'Not Available'}")
    return available
