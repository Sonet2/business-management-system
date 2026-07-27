from order_blueprint import OrderBlueprint

class OrderManager:
    def __init__(self, route_calculator):
        self.route_calculator = route_calculator

    def collect_order(self, material_manager):
        name = input("Podaj imię: ")
        surname = input("Podaj nazwisko: ")
        address = input("Podaj adres dostawy: ")
        route_info = self.route_calculator.get_route_info(address)
        if route_info is None:
            print("Nie można obliczyć trasy. Sprawdź poprawność adresu.")
            return None
        material_data = material_manager.collect_order()
        order = OrderBlueprint(name, surname, route_info, material_data)
        return order