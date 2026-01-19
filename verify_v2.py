import sys
import os
sys.path.append(os.getcwd())

from core.agent import Agent
import tools.system
import tools.browser
import tools.filesystem
import tools.content
import logging

# Configure logging to stdout
logging.basicConfig(level=logging.ERROR)

def test_v2():
    print("Testing Phase 2 Tools...")
    agent = Agent()
    
    # Test 1: Write File
    print("\n--- Test 1: Write File ---")
    agent.run("create a file named hello.txt with content 'Hello world from Jarvis'")
    
    # Test 2: Read File
    print("\n--- Test 2: Read File ---")
    agent.run("read the file hello.txt")
    
    # Test 3: Web Scrape
    print("\n--- Test 3: Scrape Web ---")
    agent.run("scrape the content of https://example.com")

if __name__ == "__main__":
    test_v2()
