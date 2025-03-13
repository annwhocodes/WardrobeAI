from crewai import Task
import logging
from agents.wardrobe_check_agent import WardrobeCheckAgent  # Import the WardrobeAgent class

logging.basicConfig(level=logging.INFO)

class CheckWardrobeTask:
    def __init__(self):
        wardrobe_agent = WardrobeCheckAgent().create_agent()

        self.task = Task(
            name="CheckWardrobeTask",
            description="Check the user's virtual wardrobe and find matching outfits.",
            agent=wardrobe_agent,  # Assign the dynamically created agent
            expected_output="A list of available outfits that match the user's preference.",
            callback=lambda result: logging.info(f"Wardrobe check result: {result}")
        )
