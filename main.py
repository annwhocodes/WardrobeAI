from workflows.crew_workflow import WardrobeWorkflow
import logging
import asyncio

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    # Create an instance of WardrobeWorkflow
    wardrobe_workflow = WardrobeWorkflow()
    
    # Run the workflow
    try:
        result = wardrobe_workflow.run_crew_workflow()
        logging.info(f"Workflow Result: {result}")
    except Exception as e:
        logging.error(f"Error running workflow: {e}")
        import traceback
        traceback.print_exc()