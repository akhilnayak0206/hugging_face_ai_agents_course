import os
from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel

# Initialize the search tool
search_tool = DuckDuckGoSearchTool()

# Initialize the model
HF_TOKEN = os.environ.get("HF_TOKEN")

if not HF_TOKEN:
    print("ERROR: HF_TOKEN environment variable not set!")
    exit(1)

model = InferenceClientModel(model_id="moonshotai/Kimi-K2.5", token=HF_TOKEN)

agent = CodeAgent(
    model=model,
    tools=[search_tool],
    additional_authorized_imports=["os", "json", "requests"],
)

# Test with a simple search
print("Testing agent with simple search...")
try:
    response = agent.run("Search for 'iran war'")
    print("SUCCESS:")
    print(response)
except Exception as e:
    print(f"ERROR: {e}")
