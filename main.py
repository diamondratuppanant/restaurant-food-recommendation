from bill_tracker import BillTracker

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import json
from pathlib import Path

menu_path = Path(__file__).parent / "data" / "menu.json"
with open(menu_path, "r") as file:
    full_menu = json.load(file)

menu_data = full_menu["items"]

tracker = BillTracker()
load_dotenv()

@tool
def display_menu() -> list:
    """Displays the menu to the user."""
    print("Fetching menu...")
    if not menu_data:
        return "The menu is currently empty."
    return menu_data





@tool
def add_to_bill(item: str) -> str:
    """If the user asks to add an item to the bill"""
    print("adding to bill...")
    for food in menu_data:
        if food["name"].lower().strip() == item.lower().strip():
            tracker.add(food)
            return f"{food['name']} has been added to the bill."
    return "That item is not on the menu."

@tool
def ask_for_bill() -> str:
    """If the user asks to see the bill"""
    print("retrieving bill...")
    return tracker.summary()

@tool
def remove_from_bill(item: str) -> str:
    """Removes an item from the user's bill."""
    print("removing from bill...")
    removed = tracker.remove(item)
    if removed:
        return f"{removed['name']} has been removed from the bill."
    return "That item is not on your bill."

def main():
    model = ChatOpenAI(temperature=0)


    tools=[display_menu,add_to_bill, ask_for_bill, remove_from_bill]
    agent_executor = create_react_agent(model, tools)

    print("Hello! Welcome to Sushi Naiya")
    print("Feel free to ask me about the menu. ", end="")

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
