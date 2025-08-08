# This file marks the Rylee package directory.
# You can import submodules such as audio_tools and agent from here.
# Import tools and agents submodules for convenience (absolute imports only)
from llm.tools.call_agent import call_agent
from llm import agents

import os

os.environ["OPENAI_API_KEY"] = "sk-proj-" # NOTE: No real key is needed. This is a work around to make Google ADK work with the tool calling models.
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"