import os, json
import logging
from typing import Annotated, Any, Sequence

from langchain_core.runnables import RunnableConfig
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel
from . import tool

# Setup logging (as you had)
_LOGGER = logging.getLogger(__name__)
# Configure logging if not already configured
if not _LOGGER.hasHandlers():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

_MAX_LLM_RETRIES = 3

llm = ChatNVIDIA(
    base_url="http://35.237.67.2:8000/v1",
    model="nvidia/NVIDIA-Nemotron-Nano-9B-v2", 
    temperature=0.0,
    api_key="no-key-required",
    max_completion_tokens=32
)

# Bind the new auto.dev tool
llm_with_tools = llm.bind_tools([tool.search_auto_dev])


# Define the new state for the graph
class AutoDevState(BaseModel):
    """
    State for the auto.dev vehicle search agent.
    
    Attributes:
        make: The vehicle manufacturer.
        model: The vehicle model.
        year: The model year.
        zip_code: The ZIP code for the search area.
        distance: The search radius in miles.
        messages: A list of messages in the chat.
    """
    make: str
    model: str
    year: int
    zip_code: str
    distance: int = 25  # Default distance if not provided
    messages: Annotated[Sequence[Any], add_messages] = []


async def tool_node(state: AutoDevState):
    """
    Executes tool calls present in the last message.
    (This function's logic remains the same)
    """
    _LOGGER.info("Executing tool calls.")
    outputs = []
    for tool_call in state.messages[-1].tool_calls:
        _LOGGER.info("Executing tool call: %s", tool_call["name"])
        # getattr dynamically finds the tool (e.g., search_auto_dev)
        tool = getattr(tools, tool_call["name"])
        tool_result = await tool.ainvoke(tool_call["args"])
        outputs.append(
            {
                "role": "tool",
                "content": json.dumps(tool_result),
                "name": tool_call["name"],
                "tool_call_id": tool_call["id"],
            }
        )
    return {"messages": outputs}


async def call_model(
    state: AutoDevState,
    config: RunnableConfig,
) -> dict[str, Any]:
    """
    Calls the LLM. On the first run, it's given a prompt to trigger the tool.
    On subsequent runs, it's given tool output to summarize.
    """
    _LOGGER.info("Calling model.")
    
    # If this is the first call (no messages), create the initial prompt.
    # Otherwise, just use the message history (which includes tool output).
    if len(state.messages) == 0:
        _LOGGER.info("Generating initial tool-triggering prompt.")
        # This is the prompt that tells Nemotron to use its tool.
        # You can customize this prompt.
        user_prompt = (
            f"Please find car listings for a {state.year} {state.make} {state.model} "
            f"near zip code {state.zip_code} within {state.distance} miles. "
            f"Use the search_auto_dev tool."
        )
        messages = [
            {"role": "system", "content": "/no_think"}, # As in your original code
            {"role": "user", "content": user_prompt}
        ]
    else:
        _LOGGER.info("Summarizing tool output.")
        # On the second pass, the state.messages list already contains
        # the user prompt AND the tool's JSON output.
        messages = [{"role": "system", "content": "/no_think"}] + list(state.messages)

    for count in range(_MAX_LLM_RETRIES):
        response = await llm_with_tools.ainvoke(messages, config)

        if response:
            return {"messages": [response]}

        _LOGGER.debug(
            "Retrying LLM call. Attempt %d of %d", count + 1, _MAX_LLM_RETRIES
        )

    raise RuntimeError(f"Failed to call model after {count + 1} attempts.")


def has_tool_calls(state: AutoDevState) -> bool:
    """
    Check if the last message has tool calls.
    (This function's logic remains the same)
    """
    messages = state.messages
    if not messages:
        return False
    last_message = messages[-1]
    return bool(last_message.tool_calls)


# --- Build the Graph ---
# Use the new AutoDevState
workflow = StateGraph(AutoDevState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    has_tool_calls,
    {
        True: "tools",
        False: END,
    },
)
workflow.add_edge("tools", "agent")
graph = workflow.compile()

# --- Example of how to run your graph ---
import asyncio

async def run_graph():
    _LOGGER.info("Starting graph run...")
    initial_input = {
        "make": "Toyota",
        "model": "Camry",
        "year": 2025,
        "zip_code": "75080",
        "distance": 10
    }
    
    final_state = await graph.ainvoke(initial_input)
    
    _LOGGER.info("Graph run complete.")
    # The final message will be Nemotron's summary of the JSON output
    print("\n--- Final Response ---")
    print(final_state['messages'][-1].content)

