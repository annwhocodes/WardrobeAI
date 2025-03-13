from crewai import Task
import logging
from agents.outfit_selection_agent import OutfitSelectionAgent  # Import the OutfitAgent class

logging.basicConfig(level=logging.INFO)

class SuggestOutfitTask:
    def __init__(self):
        # Create the outfit selection agent
        outfit_agent = OutfitSelectionAgent().create_agent()

        self.task = Task(
            name="SuggestOutfitTask",
            description="Suggest the best outfit based on weather and available wardrobe items.",
            agent=outfit_agent,  # Assign the dynamically created agent
            expected_output="A recommended outfit based on weather and wardrobe data.",
            callback=lambda result: logging.info(f"Suggested outfit: {result}")
        )
