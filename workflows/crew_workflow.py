from crewai import Flow
from crewai.flow import start, listen, router
from workflows.crew_definition import WardrobeCrew
import logging

logging.basicConfig(level=logging.INFO)

class WardrobeWorkflow(Flow):
    def __init__(self):
        super().__init__()
        
        self.crew_definition = WardrobeCrew()
        
        logging.info("WardrobeWorkflow initialized.")
    
    @start
    def start_workflow(self):
        """
        Entry point of the workflow. Starts with fetching weather data.
        """
        logging.info("Starting workflow with FetchWeatherTask.")
        result = self.crew_definition.fetch_weather_task.execute()
        logging.info(f"Task executed with result: {result}")
        return {"weather_data": result}
    
    @listen("weather_data")
    def process_weather(self, weather_data):
        """
        Listens for weather data and routes it to the search task.
        """
        logging.info(f"Weather data received: {weather_data}")
        return self.crew_definition.search_task
    
    @listen("search_result")
    def process_search(self, search_result):
        """
        Listens for search results and routes it to the wardrobe check task.
        """
        logging.info(f"Search results received: {search_result}")
        return self.crew_definition.check_wardrobe_task
    
    @listen("wardrobe_result")
    def process_wardrobe(self, wardrobe_result):
        """
        Listens for wardrobe check results and routes it to the outfit suggestion task.
        """
        logging.info(f"Wardrobe data received: {wardrobe_result}")
        return self.crew_definition.suggest_outfit_task
    
    
    def run_crew_workflow(self, initial_context=None):
        """
        Executes the crew's workflow using kickoff().
        """
        logging.info("Running workflow.")
        if initial_context is None:
            initial_context = {}
        return self.kickoff(initial_context)
    


    