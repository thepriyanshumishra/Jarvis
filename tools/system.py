from tools.registry import ToolRegistry
from operating_system.macos import MacOS

# Initialize OS interface (in a real app, detect OS)
os_interface = MacOS()

@ToolRegistry.register(name="open_app", description="Opens a local application by name. Args: app_name")
def open_app(app_name: str) -> str:
    if os_interface.open_app(app_name):
        return f"Successfully opened {app_name}"
    else:
        return f"Failed to open {app_name}"

@ToolRegistry.register(name="open_url", description="Opens a URL in the default browser. Args: url")
def open_url(url: str) -> str:
    if os_interface.open_url(url):
        return f"Successfully opened {url}"
    else:
        return f"Failed to open {url}"
