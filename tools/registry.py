from typing import Callable, Dict, Any, Optional
from core.schemas import Action

class ToolRegistry:
    _registry: Dict[str, Callable] = {}
    _metadata: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def register(cls, name: str, description: str):
        def decorator(func: Callable):
            cls._registry[name] = func
            cls._metadata[name] = {
                "name": name,
                "description": description,
            }
            return func
        return decorator

    @classmethod
    def get_tool(cls, name: str) -> Optional[Callable]:
        return cls._registry.get(name)

    @classmethod
    def list_tools(cls) -> Dict[str, Dict[str, Any]]:
        return cls._metadata
    
    @classmethod
    def execute(cls, action: Action) -> Any:
        tool = cls.get_tool(action.tool_name)
        if not tool:
            raise ValueError(f"Tool '{action.tool_name}' not registered")
        return tool(**action.args)
