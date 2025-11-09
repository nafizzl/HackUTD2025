# import os, json
# import logging
# from typing import Annotated, Any, Sequence

# from langchain_core.runnables import RunnableConfig
# from langchain_nvidia_ai_endpoints import ChatNVIDIA
# from langgraph.graph import END, START, StateGraph
# from langgraph.graph.message import add_messages
# from pydantic import BaseModel
# from . import tool

# # Setup logging (as you had)
# _LOGGER = logging.getLogger(__name__)
# # Configure logging if not already configured
# if not _LOGGER.hasHandlers():
#     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# _MAX_LLM_RETRIES = 3

# llm = ChatNVIDIA(
#     base_url="http://35.237.67.2:8000/v1",
#     model="nvidia/NVIDIA-Nemotron-Nano-9B-v2", 
#     temperature=0.0,
#     api_key="no-key-required",
#     max_completion_tokens=32
# )
# # Bind the new auto.dev tool
# llm_with_tools = llm.bind_tools([tool.search_auto_dev])


# # Define the new state for the graph
# class AutoDevState(BaseModel):
#     """
#     State for the auto.dev vehicle search agent.
    
#     Attributes:
#         make: The vehicle manufacturer.
#         model: The vehicle model.
#         year: The model year.
#         zip_code: The ZIP code for the search area.
#         distance: The search radius in miles.
#         messages: A list of messages in the chat.
#     """
#     make: str
#     model: str
#     year: int
#     zip_code: str
#     distance: int = 25  # Default distance if not provided
#     messages: Annotated[Sequence[Any], add_messages] = []


# async def tool_node(state: AutoDevState):
#     """
#     Executes tool calls present in the last message.
#     (This function's logic remains the same)
#     """
#     _LOGGER.info("Executing tool calls.")
#     outputs = []
#     for tool_call in state.messages[-1].tool_calls:
#         _LOGGER.info("Executing tool call: %s", tool_call["name"])
#         # getattr dynamically finds the tool (e.g., search_auto_dev)
#         tool = getattr(tools, tool_call["name"])
#         tool_result = await tool.ainvoke(tool_call["args"])
#         outputs.append(
#             {
#                 "role": "tool",
#                 "content": json.dumps(tool_result),
#                 "name": tool_call["name"],
#                 "tool_call_id": tool_call["id"],
#             }
#         )
#     return {"messages": outputs}


# async def call_model(
#     state: AutoDevState,
#     config: RunnableConfig,
# ) -> dict[str, Any]:
#     """
#     Calls the LLM. On the first run, it's given a prompt to trigger the tool.
#     On subsequent runs, it's given tool output to summarize.
#     """
#     _LOGGER.info("Calling model.")
    
#     # If this is the first call (no messages), create the initial prompt.
#     # Otherwise, just use the message history (which includes tool output).
#     if len(state.messages) == 0:
#         _LOGGER.info("Generating initial tool-triggering prompt.")
#         # This is the prompt that tells Nemotron to use its tool.
#         # You can customize this prompt.
#         user_prompt = (
#             f"Please find car listings for a {state.year} {state.make} {state.model} "
#             f"near zip code {state.zip_code} within {state.distance} miles. "
#             f"Use the search_auto_dev tool."
#         )
#         messages = [
#             {"role": "system", "content": "/no_think"}, # As in your original code
#             {"role": "user", "content": user_prompt}
#         ]
#     else:
#         _LOGGER.info("Summarizing tool output.")
#         # On the second pass, the state.messages list already contains
#         # the user prompt AND the tool's JSON output.
#         messages = [{"role": "system", "content": "/no_think"}] + list(state.messages)

#     for count in range(_MAX_LLM_RETRIES):
#         response = await llm_with_tools.ainvoke(messages, config)

#         if response:
#             return {"messages": [response]}

#         _LOGGER.debug(
#             "Retrying LLM call. Attempt %d of %d", count + 1, _MAX_LLM_RETRIES
#         )

#     raise RuntimeError(f"Failed to call model after {count + 1} attempts.")


# def has_tool_calls(state: AutoDevState) -> bool:
#     """
#     Check if the last message has tool calls.
#     (This function's logic remains the same)
#     """
#     messages = state.messages
#     if not messages:
#         return False
#     last_message = messages[-1]
#     return bool(last_message.tool_calls)


# # --- Build the Graph ---
# # Use the new AutoDevState
# workflow = StateGraph(AutoDevState)

# workflow.add_node("agent", call_model)
# workflow.add_node("tools", tool_node)

# workflow.add_edge(START, "agent")
# workflow.add_conditional_edges(
#     "agent",
#     has_tool_calls,
#     {
#         True: "tools",
#         False: END,
#     },
# )
# workflow.add_edge("tools", "agent")
# graph = workflow.compile()

# # --- Example of how to run your graph ---
# import asyncio

# async def run_graph():
#     _LOGGER.info("Starting graph run...")
#     initial_input = {
#         "make": "Toyota",
#         "model": "Camry",
#         "year": 2025,
#         "zip_code": "75080",
#         "distance": 10
#     }
    
#     final_state = await graph.ainvoke(initial_input)
    
#     _LOGGER.info("Graph run complete.")
#     # The final message will be Nemotron's summary of the JSON output
#     print("\n--- Final Response ---")
#     print(final_state['messages'][-1].content)

# if __name__ == "__main__":
#     asyncio.run(run_graph())

import os
import asyncio
import logging
from typing import Annotated, Any, Sequence
from langchain_core.runnables import RunnableConfig
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, SystemMessage

# --- Logging Setup ---
_LOGGER = logging.getLogger(__name__)
# Configure logging if not already configured to see INFO messages
if not _LOGGER.hasHandlers():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

_MAX_LLM_RETRIES = 3

# --- 1. LLM Initialization (Connecting to Nemotron) ---
# NOTE: This uses the cloud IP from your last successful CURL test 
# and assumes your firewall issue is resolved for port 8000.
NIM_BASE_URL = "http://35.237.67.2:8000/v1" 

llm = ChatNVIDIA(
    base_url=NIM_BASE_URL,
    model="nvidia/NVIDIA-Nemotron-Nano-9B-v2", 
    temperature=0.0,
    # Set to a placeholder string for self-hosted NIMs
    api_key="no-key-required",
    max_completion_tokens=4000
)

# --- 2. State Definition ---
# A minimal state to satisfy LangGraph's requirement for a shared state object.
class ArithmeticState(BaseModel):
    messages: Annotated[Sequence[Any], add_messages] = []

# --- 3. Graph Node (The Logic) ---
async def call_model_two_plus_two(
    state: ArithmeticState,
    config: RunnableConfig,
) -> dict[str, Any]:
    """
    Asks the LLM to calculate 2 + 2 to test the connection.
    """
    _LOGGER.info("Calling model with fixed arithmetic query: 2 + 2.")
    
    # Define the simple prompt payload
    messages = [
        SystemMessage(content="You are a precise, one-sentence arithmetic assistant."),
        HumanMessage(content="What is the result of 2 + 2?")
    ]
    
    for count in range(_MAX_LLM_RETRIES):
        try:
            # Invoke the model (using the non-tool-bound LLM instance)
            response = await llm.ainvoke(messages, config)
            
            if response:
                _LOGGER.info(f"Model response received: {response.content.strip()}")
                return {"messages": [response]}

        except Exception as e:
            _LOGGER.warning(
                f"LLM call failed (Attempt {count + 1} of {_MAX_LLM_RETRIES}): {e}"
            )
            # If all retries fail, a RuntimeError will be raised by LangGraph's runner

    raise RuntimeError(f"Failed to call model after {_MAX_LLM_RETRIES} attempts.")


# --- 4. Graph Construction and Compilation ---

workflow = StateGraph(ArithmeticState)

# Add the single node
workflow.add_node("test_agent", call_model_two_plus_two)

# Define the flow: START -> test_agent -> END
workflow.add_edge(START, "test_agent")
workflow.add_edge("test_agent", END)

# Compile the final graph
graph = workflow.compile()

# --- 5. Main Execution ---

async def run_graph():
    """Executes the compiled graph with an empty initial input."""
    _LOGGER.info("Starting Nemotron connection test graph...")
    
    # The graph expects a state object, even if it's empty for this test
    initial_input = {} 
    
    try:
        final_state = await graph.ainvoke(initial_input)
        
        # Display the result from the LLM
        # print("\n--- Final Connection Test Result ---")
        # print("LLM Response:", final_state['messages'][-1].content.strip())
        # print("----------------------------------")
        
    except Exception as e:
        _LOGGER.error(f"Graph execution failed: {e}")
        print("\n--- Connection Failed ---")
        print("Please check your cloud VM's IP, firewall rules, and NIM status (port 8000).")

if __name__ == "__main__":
    # Ensure this runs in an async event loop
    asyncio.run(run_graph())