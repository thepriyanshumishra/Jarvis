import json
from typing import List, Optional
from .schemas import Step, Action, Observation
from .planner import Planner
from llm.client import LLMClient
from llm.prompts import AGENT_SYSTEM_PROMPT
from tools.registry import ToolRegistry
import logging

class Agent:
    def __init__(self):
        self.llm = LLMClient()
        self.planner = Planner(self.llm)
        self.history: List[Step] = []
        self.logger = logging.getLogger("agent")

    def run(self, input_text: str):
        self.logger.info(f"Starting agent with input: {input_text}")
        
        # 1. Plan
        plan = self.planner.create_plan(input_text)
        self.logger.info(f"Generated plan: {plan.steps}")
        
        for step_desc in plan.steps:
            self.execute_step(step_desc)

    def execute_step(self, step_description: str):
        # Construct context from history
        context = "\n".join([f"Previous step: {s.thought} -> {s.observation}" for s in self.history])
        
        messages = [
            {"role": "system", "content": AGENT_SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nCurrent Task: {step_description}\n\nDecide the next action. Return JSON with 'thought', 'tool_name', 'args'."}
        ]
        
        response = self.llm.chat(messages, format="json")
        
        try:
            data = json.loads(response)
            thought = data.get("thought", "")
            tool_name = data.get("tool_name")
            args = data.get("args", {})
            
            action = None
            if tool_name:
                action = Action(tool_name=tool_name, args=args)
            
            # Execute
            observation = None
            if action:
                try:
                    self.logger.info(f"Executing tool: {tool_name} with args: {args}")
                    result = ToolRegistry.execute(action)
                    observation = Observation(tool_name=tool_name, output=str(result))
                except Exception as e:
                    self.logger.error(f"Tool execution failed: {e}")
                    observation = Observation(tool_name=tool_name, output=str(e), status="error", error_message=str(e))
            
            step = Step(
                step_id=len(self.history) + 1,
                thought=thought,
                action=action,
                observation=observation
            )
            self.history.append(step)
            self.logger.info(f"Step completed: {thought}")
            
        except json.JSONDecodeError:
            self.logger.error("Failed to parse LLM response")
