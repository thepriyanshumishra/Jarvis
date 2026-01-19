from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Literal

class Action(BaseModel):
    """Represents an action to be taken by the agent."""
    tool_name: str = Field(..., description="The name of the tool to execute")
    args: Dict[str, Any] = Field(default_factory=dict, description="Arguments for the tool")

class Observation(BaseModel):
    """Represents the result of an action."""
    tool_name: str
    output: Any
    status: Literal["success", "error"] = "success"
    error_message: Optional[str] = None

class Step(BaseModel):
    """Represents a single step in the agent's reasoning loop."""
    step_id: int
    thought: str = Field(..., description="The agent's reasoning")
    action: Optional[Action] = None
    observation: Optional[Observation] = None
    is_final: bool = False
    final_answer: Optional[str] = None

class Plan(BaseModel):
    """Represents the high-level plan decomposed into steps."""
    original_goal: str
    steps: List[str] = Field(..., description="List of high-level sub-tasks")
