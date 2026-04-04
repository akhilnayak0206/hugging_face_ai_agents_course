#!/usr/bin/env python3

import os
from smolagents import DuckDuckGoSearchTool


def test_search():
    print("Testing DuckDuckGo search tool...")

    # Initialize the search tool
    search_tool = DuckDuckGoSearchTool()

    # Test different queries
    test_queries = [
        "iran war",
        "iran conflict",
        "iran history",
        "test search",
        "python programming",
    ]

    for query in test_queries:
        print(f"\n--- Testing query: '{query}' ---")
        try:
            result = search_tool.forward(query)
            print(
                f"SUCCESS: {result[:200]}..."
                if len(str(result)) > 200
                else f"SUCCESS: {result}"
            )
        except Exception as e:
            print(f"ERROR: {e}")


if __name__ == "__main__":
    test_search()
