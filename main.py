from bill_tracker import BillTracker

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

tracker = BillTracker()
load_dotenv()

@tool
def display_menu() -> list:
    """Displays the menu to the user."""
    print("Fetching menu...")
    return tracker.display()

@tool
def display_full_menu() -> list:
    """this is an index for the AI to reference tags and ingredients for the user. this is not to be shown if the user asks for the menu"""
    print("fetching details")
    return tracker.display_menu()

@tool
def add_to_bill(item: str) -> str:
    """If the user asks to add an item to the bill"""
    print("adding to bill...")
    tracker.add(item)

@tool
def ask_for_bill() -> list:
    """If the user asks to see the bill"""
    print("retrieving bill...")
    return tracker.summary()

@tool
def remove_from_bill(item: str) -> str:
    """Removes an item from the user's bill."""
    print("removing from bill...")
    tracker.remove(item)

def main():
    model = ChatOpenAI(temperature=0)

    tools=[display_menu,add_to_bill, ask_for_bill, remove_from_bill, display_full_menu]
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
