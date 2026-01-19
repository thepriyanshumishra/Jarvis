import sys
import logging
from core.agent import Agent
# Import tools to register them
import tools.system
import tools.browser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/agent.log")
    ]
)

def main():
    print("Initializing Jarvis...")
    agent = Agent()
    print("Jarvis initialized. Type 'exit' to quit.")
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            if not user_input.strip():
                continue
                
            agent.run(user_input)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
