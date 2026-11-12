from warehouse_management import WarehouseManager, Warehouse
from wood_catalog import WoodCatalog
from validators import Validator
from database import Database

class Menu:
    def __init__(self, catalog, warehouse, warehouse_manager, validator, loose_material_manager, truss_manager, fuel, order_manager, truss_repository, loose_material_repository, database):
        self.catalog = catalog
        self.warehouse = warehouse
        self.warehouse_manager = warehouse_manager
        self.validator = validator
        self.loose_material_manager = loose_material_manager
        self.truss_manager = truss_manager
        self.fuel = fuel
        self.order_manager = order_manager
        self.truss_repository = truss_repository
        self.loose_material_repository = loose_material_repository
        self.database = database

    def display_menu(self):
        print("Wybierz opcję:")
        print("0. Wyjście z programu")
        print("1. Obsługa Magazynu")
        print("2. Zamówienie dla klienta")
        output = input("Wprowadź numer opcji: ")
        return output
    
    def get_user_choice(self, output):
        if output == "1":
            self.warehouse_option()
        elif output == "2":
            self.order_option()
        elif output == "0":
            print("Zamknięcie programu.")
        else:
            print("Nieprawidłowa opcja. Spróbuj ponownie.")

    def warehouse_option(self):
        
        while True:
            print("Wybrano opcję 1: Obsługa Magazynu")
            print("Wybierz działanie:")
            print("0. Powrót do menu głównego")
            print("1. Dodaj materiał do magazynu")
            print("2. Usuń materiał z magazynu")
            print("3. Wyświetl zawartość magazynu")
            warehouse_choice = input("Wprowadź numer opcji: ")
            
            if warehouse_choice == "1":
                self.warehouse_manager.add_to_warehouse()
            elif warehouse_choice == "2":
                self.warehouse_manager.delete_from_warehouse()
            elif warehouse_choice == "3":
                self.warehouse.display_warehouse()
            elif warehouse_choice == "0":
                break
            else:
                print("Nieprawidłowa opcja. Spróbuj ponownie.")

        
    def order_option(self):
        while True:
            print("Wybrano opcję 2: Zamówienie dla klienta")
            print("Wybierz działanie:")
            print("0. Powrót do menu głównego")
            print("1. Materiał luźny")
            print("2. Więźba dachowa")
            order_choice = input("Wprowadź numer opcji: ")
            if order_choice == "1":
                print("Wybrano opcje 1: Materiał luźny")
                order = self.order_manager.collect_order(self.loose_material_manager)
                if order is not None:
                    self.loose_material_repository.add_order(order)
            elif order_choice == "2":
                print("Wybrano opcje 2: Więźba dachowa")
                order = self.order_manager.collect_order(self.truss_manager)
                if order is not None:
                    self.truss_repository.add_order(order)
            elif order_choice == "0":
                break
            else:
                print("Nieprawidłowa opcja. Spróbuj ponownie.")

if __name__ == "__main__":
    database = Database(None)
    connection = database.connect()
    catalog = WoodCatalog(connection)
    warehouse = Warehouse(connection)
    validator = Validator()
    warehouse_manager = WarehouseManager(catalog, validator, warehouse)


    menu = Menu(catalog, warehouse, warehouse_manager, validator, loose_material_manager, truss_manager, fuel, order_manager, truss_repository, loose_material_repository, database)
    while True:
        output = menu.display_menu()
        menu.get_user_choice(output)
        if output == "0":
            break
        
