from database import Database
from fuel import Fuel
from wood_catalog import WoodCatalog
from datetime import datetime
from blueprints import Blueprints
from truss_manager import TrussManager
from customer_delivery import CustomerManager, DeliveryLocationManager

class Order:
    def __init__(self, connection, catalog, fuel):
        self.connection = connection
        self.catalog = catalog
        self.fuel = fuel

    def get_customer_id(self):
        results = self.connection.execute("""
        SELECT customers.id, customers.customer_type, customers.first_name, customers.last_name, customers.company_name 
        FROM customers """).fetchall()
        customers = []
        for entry in results:
            if entry[1] == "PERSON":
                description = (f"Id:{entry[0]} Imie:{entry[2]} Nazwisko:{entry[3]}")
            elif entry[1] == "COMPANY":
                description = (f"Id:{entry[0]} Nazwa firmy:{entry[4]}")
            customers.append((entry[0], description))
        return customers

    def get_delivery_locations(self, customer_id):
        results = self.connection.execute("""
            SELECT delivery_locations.id, delivery_locations.name, delivery_locations.address
            FROM delivery_locations
            WHERE delivery_locations.customer_id = ?""", (customer_id,)).fetchall()
        delivery_locations = []
        for entry in results:
            description = f"Id:{entry[0]} Nazwa:{entry[1]} Adres:{entry[2]}"
            delivery_locations.append((entry[0], description))
        return delivery_locations

    def get_delivery_distance(self, delivery_location_id):
        results = self.connection.execute("""
            SELECT distance 
            FROM delivery_locations 
            WHERE id = ?""", (delivery_location_id,)).fetchone()
        return results[0] if results else None

    def set_created_at(self):
        from datetime import datetime
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return created_at
  
    def create_orders(self, customer_id, delivery_location_id, order_type, status, created_at, delivery_date, fuel_cost_grosze, fuel_consumption):
        
        result = self.connection.execute("""
        INSERT INTO orders (customer_id, delivery_location_id, order_type, status, created_at, delivery_date, fuel_cost_grosze, fuel_consumption)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (customer_id, delivery_location_id, order_type, status, created_at, delivery_date, fuel_cost_grosze, fuel_consumption))
        return result.lastrowid 

    def add_order_items(self, order_id, material_id, m3_quantity, length, dimensions, price_per_m3_grosze):
        result = self.connection.execute("""
        INSERT INTO order_items (order_id, material_id, m3_quantity, length, dimensions, price_per_m3_grosze, line_total_grosze)
        VALUES(?,?,?,?,?,?,0)""", (order_id, material_id, m3_quantity, length, dimensions, price_per_m3_grosze))
        return result


class OrderManager:
    def __init__(self, validator, order, catalog, truss_manager, blueprints, fuel, customer_manager, delivery_location_manager):
        self.validator = validator
        self.order = order
        self.catalog = catalog
        self.truss_manager = truss_manager
        self.blueprints = blueprints
        self.fuel = fuel
        self.customer_manager = customer_manager
        self.delivery_location_manager = delivery_location_manager

    def collect_one_item(self):
        return self.blueprints.wood_selection()
    
    def print_items(self, items):
        for index, item in enumerate(items, start=1):
            category, subcategory, specie, price, m3_quantity, length, dimensions = item
            print(f"Id {index}: Kategoria: {category}, Podkategoria: {subcategory}, Gatunek: {specie}, Cena za m3: {(price / 100):.2f} zł, Ilość w m3: {m3_quantity}, Długość: {length}, Wymiary: {dimensions}")
                                            
    def ask_next_step(self):
        choice = self.validator.select_option_from_list(["Dodaj kolejną pozycję", "Usuń ostatnią pozycje", "Potwierdź zamówienie", "Anuluj  zamówienie"], "Wybierz opcję: ")
        if choice == "Dodaj kolejną pozycję":
            return "add"
        elif choice == "Usuń ostatnią pozycje":
            return "remove"
        elif choice == "Potwierdź zamówienie":
            return "confirm"
        elif choice == "Anuluj  zamówienie":
            return "cancel"

    def collect_loose_items(self):
        items = [self.collect_one_item()]
        while True:
            self.print_items(items)
            choice = self.ask_next_step()
            if choice == "add":
                items.append(self.collect_one_item())
            elif choice == "remove":
                items.pop()
                if not items:
                    items.append(self.collect_one_item())
            elif choice == "confirm":
                return items
            elif choice == "cancel":
                return None  

    def collect_truss_items(self):
        while True:
            truss = self.truss_manager.collect_truss()
            items = self.truss_manager.build_items(truss)
            self.print_items(items)
            choice = self.validator.select_option_from_list(["Potwierdź zamówienie", "Anuluj zamówienie", "Wpisz więźbe od nowa"], "Wybierz opcję: ")
            if choice == "Potwierdź zamówienie":
                return items
            elif choice == "Anuluj zamówienie":
                return None
            

    def create_order(self):
        customer_ids_list = self.order.get_customer_id()
        if not customer_ids_list:
            print("Brak klientów w bazie danych. Najpierw dodaj klienta.")
        
        for description in customer_ids_list:
            print(description[1])

        print("Klienta nie ma na liscie? Wpisz w ID cyfrę \"0\" aby dodac nowego klienta.")
        customer_id = self.validator.get_valid_number("Podaj ID klienta: ", int, 0)

        if customer_id == 0:
            customer_id = self.customer_manager.add_customer()

            if customer_id is None:
                print("Nie udało się dodać klienta.")
                return
        elif not any(customer_id == customer[0] for customer in customer_ids_list):
            print("Nieprawidłowy ID klienta.")
            return
        
        delivery_locations = self.order.get_delivery_locations(customer_id)
        if not delivery_locations:
            print("Brak miejsc dostawy dla tego klienta. Najpierw dodaj miejsce dostawy.")
        

        if len(delivery_locations) == 1:
            delivery_location_id = delivery_locations[0][0]
            print(f"Wybrano jedyne miejsce dostawy: {delivery_locations[0][1]}")
        else:
            for location in delivery_locations:
                print(location[1])

            print("Miejsca dostawy nie ma na liscie? Wpisz w ID cyfrę \"0\" aby dodac nowe miejsce dostawy.")
            delivery_location_id = self.validator.get_valid_number("Podaj ID miejsca dostawy: ", int, 0)
            if delivery_location_id == 0:
                delivery_location_id = self.delivery_location_manager.add_delivery_location(customer_id)
    
                if delivery_location_id is None:
                    print("Nie udało się dodać miejsca dostawy.")
                    return
            elif not any(delivery_location_id == location[0] for location in delivery_locations):
                print("Nieprawidłowy ID miejsca dostawy.")
                return
            
        oder_types = ["Materiał luźny", "Więźba dachowa"]
        for index, order_type in enumerate(oder_types, start=1):
            print(f"{index}. {order_type}")
        order_type = self.validator.get_valid_number("Wybierz typ zamówienia (1-2): ", int, 1, 2)
        if order_type == 1:
            order_type = "LOOSE"
            collected_items = self.collect_loose_items()
        else:
            order_type = "TRUSS"
            collected_items = self.collect_truss_items()
        if collected_items is None:
            print("Zamówienie anulowane.")
            return
        
        
        status = "IN_PROGRESS"
        created_at = self.order.set_created_at()
        delivery_date = self.validator.get_valid_date("Podaj datę dostawy (RRRR-MM-DD): ")
        distance = self.order.get_delivery_distance(delivery_location_id)
        if distance is None:
            print("Nie można obliczyć kosztów paliwa, brak danych o odległości.")
            return
        fuel_cost_grosze, fuel_consumption = self.fuel.calculate_from_distance(distance)
        try:
            order_id = self.order.create_orders(customer_id, delivery_location_id, order_type, status, created_at, delivery_date, fuel_cost_grosze, fuel_consumption)
            for item in collected_items:
                category, subcategory, specie, price, m3_quantity, length, dimensions = item
                material_ids = self.catalog.get_position_id(category, subcategory, specie)
                if not material_ids:
                    raise ValueError(f"Nie znaleziono materiału w katalogu: {category}, {subcategory}, {specie}")
                material_id = material_ids  [0]
                self.order.add_order_items(order_id, material_id, m3_quantity, length, dimensions, price)
            self.order.connection.commit()
        except Exception:
            self.order.connection.rollback()
            raise