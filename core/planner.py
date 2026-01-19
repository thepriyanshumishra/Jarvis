from typing import List
import json
from .schemas import Plan
from llm.client import LLMClient
from llm.prompts import PLANNER_PROMPT

class Planner:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def create_plan(self, goal: str) -> Plan:
        messages = [
            {"role": "system", "content": PLANNER_PROMPT},
            {"role": "user", "content": f"Create a step-by-step plan for: {goal}. Return JSON with a 'steps' list."}
        ]
        
        # We expect the LLM to return JSON
        response = self.llm.chat(messages, format="json")
        
        try:
            data = json.loads(response)
            steps_raw = data.get("steps", [])
            steps = []
            for s in steps_raw:
                if isinstance(s, dict):
                    # If LLM returns a dict (e.g. {"action": "..."}), convert to string
                    steps.append(str(s.get("action", s)))
                else:
                    steps.append(str(s))
            return Plan(original_goal=goal, steps=steps)
        except json.JSONDecodeError:
            # Fallback if strict JSON fails - simplistic parsing
            return Plan(original_goal=goal, steps=[response])
