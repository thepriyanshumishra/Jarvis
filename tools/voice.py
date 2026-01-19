import subprocess
from tools.registry import ToolRegistry

@ToolRegistry.register(name="speak", description="Speaks the provided text. Args: text")
def speak(text: str) -> str:
    """
    Uses macOS 'say' command to speak text.
    """
    try:
        # Use a high quality voice if available, else default
        subprocess.run(["say", text], check=True)
        return "Spoke text successfully."
    except Exception as e:
        return f"Error speaking text: {e}"
