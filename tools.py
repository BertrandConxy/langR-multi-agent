from langchain_core.tools import tool
from typing import Literal

@tool
def get_weather(city: Literal["nyc", "sf"]):
    """Retrieve weather information."""
    if city == "nyc":
        return "It might be cloudy in NYC."
    elif city == "sf":
        return "It's always sunny in SF."
    else:
        raise ValueError("Unknown city")