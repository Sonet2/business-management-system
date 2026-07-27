import json

class BaseOrderRepository:
    def __init__(self, order_file, model_class):
        self.order_file = order_file
        self.model_class = model_class
        self.orders = self.load_orders()

    def load_orders(self):
        try:
            with open(self.order_file, "r", encoding="utf-8") as f:
                raw_orders = json.load(f)
                return [self.model_class.from_dict(raw) for raw in raw_orders]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Błąd dekodowania pliku JSON. Plik może być uszkodzony.")
            return []

    def save_orders(self):
        try:
            with open(self.order_file, "w", encoding="utf-8") as f:
                json.dump([order.to_dict() for order in self.orders], f, ensure_ascii=False, indent=4)
        except OSError as e:
            print(f"Wystąpił błąd podczas zapisywania danych do pliku: {e}")

    def add_order(self, order):
        self.orders.append(order)
        self.save_orders()