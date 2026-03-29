from unit1.tools.visit_webpage import VisitWebpageTool
from unit1.tools.web_search import DuckDuckGoSearchTool as CustomDuckDuckGoSearchTool
from smolagents import (
    CodeAgent,
    InferenceClientModel,
    load_tool,
    tool,
)
import datetime
import requests
import pytz
import yaml
from unit1.tools.final_answer import FinalAnswerTool

from unit1.GradioUI import GradioUI


# Below is an example of a tool that does nothing. Amaze us with your creativity!
@tool
def my_custom_tool(
    arg1: str, arg2: int
) -> str:  # it's important to specify the return type
    # Keep this format for the tool description / args description but feel free to modify the tool
    """A tool that does nothing yet
    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return "What magic will you build ?"


@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


final_answer = FinalAnswerTool()
visit_webpage = VisitWebpageTool()
web_search = CustomDuckDuckGoSearchTool()

model = InferenceClientModel(
    max_tokens=2096,
    temperature=0.5,
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    custom_role_conversions=None,
)


# Import tool from Hub
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

agent = CodeAgent(
    model=model,
    tools=[
        final_answer,
        web_search,
        visit_webpage,
    ],  # add your tools here (don't remove final_answer)
    max_steps=6,
    verbosity_level=1,
    planning_interval=None,
    name=None,
    description=None,
)


GradioUI(agent).launch()


def main():
    GradioUI(agent).launch()


if __name__ == "__main__":
    main()
