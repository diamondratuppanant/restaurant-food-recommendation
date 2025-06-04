# bill_tracker.py
class BillTracker:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def get(self):
        return self.items

    def summary(self):
        if not self.items:
            return "Your bill is currently empty."
        total = sum(item["base_price"] for item in self.items)
        lines = [f"{item['name']}: {item['base_price']}" for item in self.items]
        lines.append(f"Total: ${total:.2f}")
        return "\n".join(lines)


    def remove(self, item_name: str):
        for i, item in enumerate(self.items):
            if item["name"].lower().strip() == item_name.lower().strip():
                del self.items[i]
                return item
        return None