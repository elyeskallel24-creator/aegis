"""Agent that orchestrates LLM and tool execution."""

from typing import Any, Dict, Optional
from src.core.llm import BaseLLMProvider, LLMResponse
from src.core.tool_registry import ToolRegistry
from src.core.governor import ResourceGovernor


class Agent:
    """Orchestrates LLM decision-making and tool execution."""

    def __init__(
        self,
        llm_provider: BaseLLMProvider,
        tool_registry: ToolRegistry,
        governor: ResourceGovernor
    ):
        self.llm = llm_provider
        self.tools = tool_registry
        self.governor = governor

    async def run(self, user_prompt: str) -> Dict[str, Any]:
        """
        Execute the agent loop: think → decide → act → return result.
        
        Args:
            user_prompt: The user's input request.
            
        Returns:
            Dictionary containing:
            - llm_response: The LLM's decision
            - tool_result: Result from tool execution (if any)
            - final_answer: The agent's final response to the user
        """
        # Step 1: LLM thinks about what to do
        async with self.governor.ai_call():
            llm_response = await self.llm.generate(user_prompt)
        
        # Step 2: Parse LLM response to determine if tool is needed
        # For now, we'll use a simple heuristic: if response mentions "use tool"
        tool_result = None
        if "use tool" in llm_response.content.lower():
            # Step 3: Execute tool (if available)
            available_tools = self.tools.list_tools()
            if available_tools:
                tool = available_tools[0]  # Use first available tool
                async with self.governor.tool_call():
                    tool_result = await tool.execute(input_value=user_prompt)
        
        # Step 4: Return structured result
        return {
            "llm_response": llm_response.content,
            "tool_result": tool_result,
            "final_answer": f"Agent processed: {user_prompt}"
        }