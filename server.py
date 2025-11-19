from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("weather")

def main():
    """Main entry point for the MCP server."""
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()

# Constants
OPENMETEO_API_BASE = "https://api.open-meteo.com/v1"
USER_AGENT = "Weather-app/1.0"

# Helper function to make a request to the Open-Meteo API
async def make_openmeteo_request(url: str) -> dict[str, Any] | None:
    """Make a request to the Open-Meteo API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return None

   

@mcp.tool()
async def get_current_weather(latitude: float, longitude: float) -> str:
    """Get the current weather for a location.

    Args:
        latitude (float): latitude of the location.
        longitude (float): longitude of the location.
    """
    url = f"{OPENMETEO_API_BASE}/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,is_day,showers,cloud_cover,wind_speed_10m,wind_direction_10m,pressure_msl,snowfall,precipitation,relative_humidity_2m,apparent_temperature,rain,weather_code,surface_pressure,wind_gusts_10m"
    data = await make_openmeteo_request(url)

    if not data:
        return "Unable to fetch current weather data for this location."
    
    # Format the weather data as a readable string
    current = data.get("current", {})
    return f"Weather at ({latitude}, {longitude}): Temperature: {current.get('temperature_2m')}°C, Conditions: {current.get('weather_code')}, Wind Speed: {current.get('wind_speed_10m')} km/h"