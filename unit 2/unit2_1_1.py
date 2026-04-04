import os
from dotenv import load_dotenv
from PIL import Image
from smolagents import (
    CodeAgent,
    GoogleSearchTool,
    InferenceClientModel,
    VisitWebpageTool,
)
import math
from typing import Optional, Tuple

from smolagents import tool

# Load environment variables from .env file
load_dotenv()


@tool
def calculate_cargo_travel_time(
    origin_coords: Tuple[float, float],
    destination_coords: Tuple[float, float],
    cruising_speed_kmh: Optional[float] = 750.0,  # Average speed for cargo planes
) -> float:
    """
    Calculate the travel time for a cargo plane between two points on Earth using great-circle distance.

    Args:
        origin_coords: Tuple of (latitude, longitude) for the starting point
        destination_coords: Tuple of (latitude, longitude) for the destination
        cruising_speed_kmh: Optional cruising speed in km/h (defaults to 750 km/h for typical cargo planes)

    Returns:
        float: The estimated travel time in hours

    Example:
        >>> # Chicago (41.8781° N, 87.6298° W) to Sydney (33.8688° S, 151.2093° E)
        >>> result = calculate_cargo_travel_time((41.8781, -87.6298), (-33.8688, 151.2093))
    """

    def to_radians(degrees: float) -> float:
        return degrees * (math.pi / 180)

    # Extract coordinates
    lat1, lon1 = map(to_radians, origin_coords)
    lat2, lon2 = map(to_radians, destination_coords)

    # Earth's radius in kilometers
    EARTH_RADIUS_KM = 6371.0

    # Calculate great-circle distance using the haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    distance = EARTH_RADIUS_KM * c

    # Add 10% to account for non-direct routes and air traffic controls
    actual_distance = distance * 1.1

    # Calculate flight time
    # Add 1 hour for takeoff and landing procedures
    flight_time = (actual_distance / cruising_speed_kmh) + 1.0

    # Format the results
    return round(flight_time, 2)


print(calculate_cargo_travel_time((41.8781, -87.6298), (-33.8688, 151.2093)))
# SERPAPI API key should be set as environment variable
# export SERPAPI_API_KEY="your_actual_api_key"
import os

# Check if HF_TOKEN is set
hf_token = os.environ.get("HF_TOKEN")
if not hf_token:
    print("ERROR: HF_TOKEN environment variable not set!")
    print("Please set it in your .env file: HF_TOKEN=your_huggingface_token")
    exit(1)

model = InferenceClientModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct", token=hf_token)


task = """Find all Batman filming locations in the world, calculate the time to transfer via cargo plane to here (we're in Gotham, 40.7128° N, 74.0060° W), and return them to me as a pandas dataframe.
Also give me some supercar factories with the same cargo plane transfer time."""

agent = CodeAgent(
    model=model,
    tools=[
        GoogleSearchTool(),
        VisitWebpageTool(),
        calculate_cargo_travel_time,
    ],
    additional_authorized_imports=["pandas"],
    max_steps=20,
)


result = agent.run(task)

print(result)
