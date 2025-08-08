from google.adk.runners import Runner
from google.adk.agents import Agent
import asyncio

async def call_agent(agent: Agent, message: str) -> str:
    """
    Calls an agent and returns the result.
    
    Args:
        agent (Agent): The agent to call.
        message (str): The message to send to the agent.
    
    Returns:
        str: The result of the agent.
    """
    return await Runner.run_async(agent, message)

def call_main_agent(message: str) -> str:
    """
    Calls the main agent and returns the result.
    
    Args:
        message (str): The message to send to the main agent.
    
    Returns:
        str: The result of the main agent.
    """
    return asyncio.run(call_agent(main_agent, message))
