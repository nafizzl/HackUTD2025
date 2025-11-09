import os
import json
import logging
import httpx 
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from dotenv import load_dotenv

_LOGGER = logging.getLogger(__name__)

# --- Configuration ---
# The key is read once at the module level (like before)
load_dotenv()  
AUTO_DEV_API_KEY = os.getenv("AUTO_DEV_API_KEY")
BASE_URL = "https://api.auto.dev/listings"

if not AUTO_DEV_API_KEY:
    _LOGGER.warning(
        "AUTO_DEV_API_KEY environment variable not set. API calls to auto.dev will fail."
    )
    # NOTE: It's good practice to ensure the LLM can't proceed if the tool is broken.
    # We rely on the code inside the function to return a structured error message.

# --- Tool Input Schema (Remains Unchanged) ---
class AutoDevInput(BaseModel):
    """Input schema for the search_auto_dev tool."""
    make: str = Field(..., description="The vehicle manufacturer (e.g., 'Toyota')")
    model: str = Field(..., description="The vehicle model (e.g., 'Camry')")
    year: int = Field(..., description="The model year (e.g., 2025)")
    zip_code: str = Field(..., description="The 5-digit US ZIP code for the search")
    distance: int = Field(..., description="The search radius in miles")

# --- The Corrected Tool Implementation ---
@tool(args_schema=AutoDevInput)
async def search_auto_dev(
    make: str, model: str, year: int, zip_code: str, distance: int
) -> str:
    """
    Searches the auto.dev API for vehicle listings based on make, model, year,
    zip code, and distance. Returns a JSON string of listings.
    """

    # 1. Properly apply the Bearer prefix and build headers at runtime
    headers = {
        'Authorization': f'Bearer {AUTO_DEV_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    # 2. Build Query Parameters
    params = {
        'make': make,
        'model': model,
        'year': year,
        'zipCode': zip_code, # 'zipCode' is camelCase for the API
        'radius': distance,
        'newAndUsed': 'new'
    }
    
    _LOGGER.info(f"Calling auto.dev API with params: {params}")

    # 3. Execute Asynchronous Request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                BASE_URL, 
                headers=headers, 
                params=params,
                timeout=15.0
            )
            
            response.raise_for_status() 
            
            # The LLM (Nemotron) will parse this raw response string
            return response.text 
    
    except httpx.HTTPStatusError as e:
        _LOGGER.error(f"HTTP error {e.response.status_code} occurred: {e}")
        # Return a structured error for the LLM to read
        return json.dumps(
            {
                "error": "HTTP Status Error", 
                "status_code": e.response.status_code, 
                "details": f"Failed to fetch data: {e.response.text[:100]}..." # Limit detail size
            }
        )
    except httpx.RequestError as e:
        _LOGGER.error(f"An error occurred while requesting: {e}")
        return json.dumps({"error": "Request Error", "details": str(e)})
    except Exception as e:
        _LOGGER.error(f"An unexpected error occurred: {e}")
        return json.dumps({"error": "Unexpected Error", "details": str(e)})