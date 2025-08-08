from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.agents import Agent
from google.genai import types # For creating message Content/Parts

async def create_session(app_name: str, user_id: str, session_id: str) -> InMemorySessionService:
    """
    Creates a session service and initializes a session for the given app, user, and session ID.
    
    Args:
        app_name (str): The name of the app.
        user_id (str): The user ID.
        session_id (str): The session ID.
    
    Returns:
        InMemorySessionService: The session service with the created session.
    """
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    print(f"Session created: App='{app_name}', User='{user_id}', Session='{session_id}'")
    return session_service

def create_runner(agent: Agent, app_name: str, session_service) -> Runner:
    """
    Creates a runner for the given agent.
    
    Args:
        agent (Agent): The agent to create a runner for.
        app_name (str): The name of the app.
        session_service (InMemorySessionService): The session service to use.
    
    Returns:
        Runner: The created runner.
    """
    runner = Runner(
        agent=agent,
        app_name=app_name,
        session_service=session_service
    )
    print(f"Runner created for App='{app_name}'")
    return runner

async def call_agent_async(query: str, runner: Runner, user_id: str, session_id: str):
    """
    Calls an agent and returns the final response.
    
    Args:
        query (str): The message to send to the agent.
        runner (Runner): The runner to use to call the agent.
        user_id (str): The user ID.
        session_id (str): The session ID.
    
    Returns:
        str: The final response from the agent.
    """
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response_text = "Agent did not produce a final response."

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response_text = (
                    f"Agent escalated: {event.error_message or 'No specific message.'}"
                )
            break

    return final_response_text

async def run_conversation(query: str, runner: Runner, user_id: str, session_id: str):
    """
    Runs a conversation with the given query.
    
    Args:
        query (str): The message to send to the agent.
        runner (Runner): The runner to use to call the agent.
        user_id (str): The user ID.
        session_id (str): The session ID.
    
    Returns:
        str: The final response from the agent.
    """
    return await call_agent_async(
        query=query,
        runner=runner,
        user_id=user_id,
        session_id=session_id
    )
