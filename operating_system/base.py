from abc import ABC, abstractmethod

class OSInterface(ABC):
    @abstractmethod
    def open_app(self, app_name: str) -> bool:
        """Opens an application by name."""
        pass
    
    @abstractmethod
    def open_url(self, url: str) -> bool:
        """Opens a URL in the default browser."""
        pass
