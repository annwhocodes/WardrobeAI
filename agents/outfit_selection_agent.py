from crewai import Agent

class OutfitSelectionAgent:
    def create_agent(self):
        return Agent(
            role="Fashion Advisor",
            goal="Suggest the best outfit based on weather and wardrobe availability.",
            backstory="You are a fashion expert who knows how to match outfits with weather conditions and personal style. You have a deep understanding of color coordination, fabric suitability, and seasonal trends.",
            verbose=True,
            allow_delegation=False
        )