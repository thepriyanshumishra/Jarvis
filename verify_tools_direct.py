import sys
import os
sys.path.append(os.getcwd())

# Direct import of tools to test logic without agent/LLM overhead
import tools.filesystem
import tools.content
from tools.registry import ToolRegistry
from core.schemas import Action

def test_tools_direct():
    print("Testing Tools Directly (No LLM)...")
    
    # Test 1: Write File
    print("\n--- Test 1: Write File ---")
    action = Action(tool_name="write_file", args={"path": "hello_direct.txt", "content": "Direct write test"})
    result = ToolRegistry.execute(action)
    print(f"Result: {result}")
    
    # Test 2: Read File
    print("\n--- Test 2: Read File ---")
    action = Action(tool_name="read_file", args={"path": "hello_direct.txt"})
    result = ToolRegistry.execute(action)
    print(f"Result: {result}")
    assert "Direct write test" in str(result)
    
    # Test 3: List Files
    print("\n--- Test 3: List Files ---")
    action = Action(tool_name="list_files", args={"path": "."})
    result = ToolRegistry.execute(action)
    print(f"Result (len): {len(str(result))}")
    assert "hello_direct.txt" in str(result)
    
    # Test 4: Web Scrape
    print("\n--- Test 4: Web Scrape ---")
    # Use a reliable, small page
    action = Action(tool_name="scrape_url", args={"url": "https://www.example.com"})
    result = ToolRegistry.execute(action)
    print(f"Result (truncated): {str(result)[:100]}...")
    assert "Example Domain" in str(result) or "Domain" in str(result)

if __name__ == "__main__":
    try:
        test_tools_direct()
        print("\nSUCCESS: All tools verified.")
    except Exception as e:
        print(f"\nFAILURE: {e}")
        import traceback
        traceback.print_exc()
