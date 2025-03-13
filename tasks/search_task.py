from crewai import Task
import logging
from agents.search_agent import SearchAgent

logging.basicConfig(level=logging.INFO)

class SearchTask:
    def __init__(self):
        # Create the search agent
        search_agent = SearchAgent().create_agent()
        
        self.task = Task(
            name="SearchTask",
            description="Search for additional information such as trending fashion or weather APIs.",
            agent=search_agent,
            expected_output="A detailed report of relevant information.",
            context=[],  # Add context if needed
            output_key="search_result",  # This should match your listener in the workflow
            callback=self._process_result
        )
    
    def _process_result(self, result):
        logging.info(f"Search results: {result}")
        # Return the result with the key that matches your listener
        return {"search_result": result}