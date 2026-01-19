from tools.registry import ToolRegistry
from operating_system.macos import MacOS

# Initialize OS interface
os_interface = MacOS()

@ToolRegistry.register(name="open_browser", description="Opens the default web browser.")
def open_browser() -> str:
    # Just opens Google as a default homepage
    if os_interface.open_url("https://www.google.com"):
        return "Browser opened."
    else:
        return "Failed to open browser."

@ToolRegistry.register(name="search_web", description="Searches the web for a query. Args: query")
def search_web(query: str) -> str:
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    if os_interface.open_url(url):
        return f"Searching for '{query}' in browser."
    else:
        return f"Failed to search for '{query}'."
