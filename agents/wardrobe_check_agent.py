from crewai import Agent

class WardrobeCheckAgent:
    def create_agent(self):
        return Agent(
            role="Wardrobe Manager",
            goal="Check the user's wardrobe for available clothing items.",
            backstory="You are an organized manager who keeps track of all clothing items in the user's wardrobe. You know exactly what items are available and their condition.",
            verbose=True,
            allow_delegation=False
        )