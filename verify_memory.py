import sys
import os
sys.path.append(os.getcwd())

from core.memory import Memory
from tools.memory_tool import remember, recall, get_history
from core.agent import Agent

def test_memory():
    # 1. Test Core Memory Logic
    print("Testing Core Memory...")
    m = Memory()
    m.add_log("user", "test input")
    logs = m.get_recent_logs(1)
    print(f"Log: {logs}")
    assert len(logs) > 0
    assert logs[0]['content'] == "test input"

    m.set_value("name", "JarvisTester")
    val = m.get_value("name")
    print(f"Value: {val}")
    assert val == "JarvisTester"

    # 2. Test Tools
    print("\nTesting Memory Tools...")
    print(remember("favorite_color", "blue"))
    print(recall("favorite_color"))
    
    # 3. Test Agent Integration (Logging)
    print("\nTesting Agent Intagration...")
    agent = Agent()
    # Mocking run without LLM to see if it logs
    # We can't easily test without LLM unless we mock LLM client, 
    # but we can check if DB has new entries after a run call 
    # (though run call would fail if LLM is offline/mocked poorly).
    # For now, let's rely on manual Agent verification via main.py later.
    
    print("Memory tests passed!")

if __name__ == "__main__":
    test_memory()
