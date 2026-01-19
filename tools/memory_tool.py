from tools.registry import ToolRegistry
from core.memory import Memory

# Initialize memory instance
memory = Memory()

@ToolRegistry.register(name="remember", description="Stores a key-value pair in memory. Args: key, value")
def remember(key: str, value: str) -> str:
    try:
        memory.set_value(key, value)
        return f"Remembered: {key} = {value}"
    except Exception as e:
        return f"Error remembering: {str(e)}"

@ToolRegistry.register(name="recall", description="Retrieves a value from memory by key. Args: key")
def recall(key: str) -> str:
    try:
        val = memory.get_value(key)
        if val:
            return f"Recalled: {key} is {val}"
        else:
            return f"I don't have a memory of '{key}'."
    except Exception as e:
        return f"Error recalling: {str(e)}"

@ToolRegistry.register(name="get_history", description="Retrieves the last N interactions. Args: limit (int)")
def get_history(limit: int = 5) -> str:
    try:
        logs = memory.get_recent_logs(limit=int(limit))
        formatted = "\n".join([f"{l['role']}: {l['content']}" for l in logs])
        return formatted if formatted else "No recent history."
    except Exception as e:
        return f"Error getting history: {str(e)}"
