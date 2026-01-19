import ollama
from typing import List, Dict, Any, Optional

class LLMClient:
    def __init__(self, model: str = "phi3:mini"):
        self.model = model

    def chat(self, messages: List[Dict[str, str]], format: Optional[str] = None) -> str:
        """
        Sends a chat request to the Ollama model.
        Args:
            messages: List of message dictionaries containing 'role' and 'content'.
            format: Optional format specification (e.g., 'json').
        Returns:
            The content of the response message.
        """
        try:
            response = ollama.chat(model=self.model, messages=messages, format=format)
            return response['message']['content']
        except Exception as e:
            # In a real app we might want to retry or fallback
            raise RuntimeError(f"LLM communication failed: {e}")
