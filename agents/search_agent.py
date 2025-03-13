from crewai import Agent

class SearchAgent:
    def create_agent(self):
        return Agent(
            role="Search Specialist",
            goal="Search for additional information such as trending fashion or weather APIs.",
            backstory="You are an expert at finding relevant information from various sources to assist in decision-making.",
            verbose=True,
            allow_delegation=False
        )