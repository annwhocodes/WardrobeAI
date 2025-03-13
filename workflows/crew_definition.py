from crewai import Crew, Agent, Task
from agents.weather_agent import WeatherAgent
from agents.outfit_selection_agent import OutfitSelectionAgent
from agents.wardrobe_check_agent import WardrobeCheckAgent
from agents.search_agent import SearchAgent
from tasks.fetch_weather_task import FetchWeatherTask
from tasks.suggest_outfit_task import SuggestOutfitTask
from tasks.check_wardrobe_task import CheckWardrobeTask
from tasks.search_task import SearchTask
import logging

logging.basicConfig(level=logging.INFO)

class WardrobeCrew:
    def __init__(self):
        self.weather_agent = WeatherAgent().create_agent()
        self.wardrobe_check_agent = WardrobeCheckAgent().create_agent()
        self.outfit_selection_agent = OutfitSelectionAgent().create_agent()
        self.search_agent = SearchAgent().create_agent()
        
        self.fetch_weather_task = FetchWeatherTask().task
        self.check_wardrobe_task = CheckWardrobeTask().task
        self.suggest_outfit_task = SuggestOutfitTask().task
        self.search_task = SearchTask().task
        
        self.crew = Crew(
            agents=[self.weather_agent, self.wardrobe_check_agent, self.outfit_selection_agent, self.search_agent],
            tasks=[self.fetch_weather_task, self.check_wardrobe_task, self.suggest_outfit_task, self.search_task]
        )
        
        logging.info("✅ WardrobeCrew initialized successfully!")
        return 
