import sys
import logging
import os
# Ensure current dir is in path
sys.path.append(os.getcwd())

from core.agent import Agent
import tools.system
import tools.browser

# Configure logging to stdout
logging.basicConfig(level=logging.INFO)

def test():
    print("Testing Agent...")
    try:
        agent = Agent()
        print("Agent initialized.")
        
        # Test 1: Simple tool
        print("\n--- Test 1: Open Browser ---")
        agent.run("open browser")
        
        # Test 2: Multi-step
        print("\n--- Test 2: Search ---")
        agent.run("search for 'python agent' on the web")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()
