import json
from typing import List, Optional
from .schemas import Step, Action, Observation
from .planner import Planner
from llm.client import LLMClient
from llm.prompts import AGENT_SYSTEM_PROMPT
from tools.registry import ToolRegistry
import logging

from core.memory import Memory

class Agent:
    def __init__(self):
        self.llm = LLMClient()
        self.planner = Planner(self.llm)
        self.history: List[Step] = []
        self.logger = logging.getLogger("agent")
        self.memory = Memory()

    def run(self, input_text: str):
        self.logger.info(f"Starting agent with input: {input_text}")
        
        # Log User Input to Memory
        self.memory.add_log("user", input_text)
        
        # Retrieve recent context (short-term memory from DB)
        # We could use this to augment the planner or execution prompts
        # current_context = self.memory.get_recent_logs(5)
        
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
                # Handle cases where LLM hallucinates list args
                if isinstance(args, list):
                    self.logger.warning(f"LLM returned list for args: {args}. Attempting to recover.")
                    # Simplistic recovery: if 1 item, maybe it's the first arg? 
                    # But we don't know the key. Safer to make it empty or error cleanly.
                    # For now, let's just warn and try to proceed with empty or error.
                    args = {} 
                
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
            
            # Log Agent Thought/Action to Memory
            self.memory.add_log("agent", f"Thought: {thought} | Action: {tool_name} | Result: {str(observation.output if observation else '')[:100]}...")
            
        except json.JSONDecodeError:
            self.logger.error("Failed to parse LLM response")
