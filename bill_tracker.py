# bill_tracker.py
import json
from enum import verify
from pathlib import Path

menu_path = Path(__file__).parent / "data" / "menu.json"
with open(menu_path, "r") as file:
    full_menu = json.load(file)

menu_data = full_menu["items"]
modifiers = full_menu["modifiers"]


class BillTracker:
    def __init__(self):
        self.items = []

    def add(self, item):
        for food in menu_data:
            if item.lower().strip() == food["name"].lower().strip():
                self.items.append(food)


    def get(self):
        return self.items

    def summary(self):
        if not self.items:
            return "Your bill is currently empty."
        total = sum(item["base_price"] for item in self.items) * 1.065
        lines = [f"{item['name']}: {item['base_price']}" for item in self.items]
        lines.append(f"Total: ${total:.2f} including tax")
        return "\n".join(lines)


    def remove(self, item_name: str):
        for i, item in enumerate(self.items):
            if item["name"].lower().strip() == item_name.lower().strip():
                del self.items[i]
                return item
        return None

    def display(self):
        name_and_price = []
        if not menu_data:
            return "There is no menu."
        else:
            for food in menu_data:
                name_and_price.append(f"{food['name']}: {food['base_price']}")
            return name_and_price

    def display_menu(self):
        return menu_data