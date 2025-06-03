from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import json
from pathlib import Path

menu_path = Path(__file__).parent / "data" / "menu.json"
with open(menu_path, "r") as file:
    menu_data = json.load(file)

load_dotenv()

@tool
def recommend_dish(preference: str) -> str:
    """Recommending a dish based on user preference such as 'cheap', 'vegan', 'no peanuts', etc"""
    recommendations = []
    print("Recommending Dishes...")
    for item in menu_data:
        if "no peanuts" in preference.lower() and "peanuts" in item["ingredients"]:
            continue
        if "cheap" in preference.lower() and item["price"] > 10:
            continue
        if any(tag in preference.lower() for tag in item["tags"]):
            recommendations.append(item["name"])
    return ", ".join(recommendations) if recommendations else "No suitable dishes found."

def display_menu(query: str) -> str:
    """If the user asks what is on the menu"""
    return menu_data

def main():
    model = ChatOpenAI(temperature=0)

    tools=[recommend_dish, display_menu]
    agent_executor = create_react_agent(model, tools)

    print("Hello! I am an AI assistant")
    print("Please ask me things to do: ", end="")

    while True:
        user_input = input("\nUSER> ").strip()

        if user_input == "quit":
            break

        print("\nAI> ", end="")
        for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")

if __name__ == "__main__":
    main()