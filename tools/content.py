import requests
from bs4 import BeautifulSoup
from tools.registry import ToolRegistry

@ToolRegistry.register(name="scrape_url", description="Scrapes text content from a URL. Args: url")
def scrape_url(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        text = soup.get_text()
        
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text[:5000] + ("..." if len(text) > 5000 else "")  # Limit output
        
    except Exception as e:
        return f"Error scraping URL: {str(e)}"
