from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from llm.tools.tools import *

# Sub-agent for programming tasks
coder_agent = Agent(
    model=LiteLlm(model="openai/gpt-oss:20b"),
    name="coder_agent",
    description="Writes and explains Python (and other) code when invoked by the main agent.",
    instruction=(
        "You are CodeR, a focused programming assistant. "
        "When invoked, produce clear, runnable code snippets. "
        "If an explanation is requested, add concise comments or prose after the code. "
        "Otherwise, return only the code block. "
        "Never call other tools."
    ),
    tools=[
        enter_cli_command
    ]
)

# main agent
main_agent = Agent(
    model=LiteLlm(model="openai/gpt-oss:20b"),
    name="main_agent",
    description=(
        "You are the main agent that talks to the user. "
    ),
    instruction=(
        "You are a Computer Assistant, a helpful voice-based home assistant. "
        "Respond concisely and conversationally. "
        "When you call tools, ALWAYS transform their raw output into a human-friendly reply. "
        "Guidelines for common data:\n"
        "- Time: get_time returns 'HH:MM:SS' in 24-hour format. Present it as either 'HH:MM' (24-hour) or 'h:MM AM/PM' based on the user's locale / request - never include the seconds.\n"
        "- Date: get_date returns 'YYYY-MM-DD'. Convert it to a readable date such as 'June 11, 2025'.\n"
        "- Weather: Summarise the important parts (temperature and conditions) and mention the city.\n"
        "Never expose raw JSON, numbers, or function_call objects."
        "If you require information refer to the available tools. "
        "If you require a location for weather or other services, use get_city. "
        "If you require a date or time, use get_date or get_time. "
        "If you don't know the user's location, use get_city. "
        "If you require a CLI command to be executed, or programming assistance, use coder_agent."
    ),
    tools=[
        get_city,
        get_date,
        get_time,
        get_current_weather,
    ],
    sub_agents=[
        coder_agent
    ]
)
