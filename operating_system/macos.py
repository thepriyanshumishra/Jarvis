import subprocess
from .base import OSInterface

class MacOS(OSInterface):
    def open_app(self, app_name: str) -> bool:
        try:
            subprocess.run(["open", "-a", app_name], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def open_url(self, url: str) -> bool:
        try:
            subprocess.run(["open", url], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
