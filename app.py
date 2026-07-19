from warehouse_management import WarehouseManager, Warehouse
from wood_catalog import WoodCatalog
from validators import Validator
from loose_material import LooseMaterialOrder, LooseMaterialManager

class Menu:
    def __init__(self, catalog, warehouse, warehouse_manager, validator, loose_material_manager):
        self.catalog = catalog
        self.warehouse = warehouse
        self.warehouse_manager = warehouse_manager
        self.validator = validator
        self.loose_material_manager = loose_material_manager

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
            warehouse_option = input("Wprowadź numer opcji: ")
            
            if warehouse_option == "1":
                self.warehouse_manager.add_to_warehouse()
            elif warehouse_option == "2":
                self.warehouse_manager.delete_from_warehouse()
            elif warehouse_option == "3":
                self.warehouse.display_warehouse()
            elif warehouse_option == "0":
                break
            else:
                print("Nieprawidłowa opcja. Spróbuj ponownie.")

        
    def order_option(self):
        print("Wybrano opcję 2: Zamówienie dla klienta")
        print("Wybierz działanie:")
        print("0. Powrót do menu głównego")
        print("1. Materiał luźny")
        print("2. Więźba dachowa")
        order_option = input("Wprowadź numer opcji: ")
        if order_option == "1":
            print("Wybrano opcje 1: Materiał luźny")
        elif order_option == "2":
            print("Wybrano opcje 2: Więźba dachowa")
        else:
            print("Nieprawidłowa opcja. Spróbuj ponownie.")

if __name__ == "__main__":
    catalog = WoodCatalog()
    warehouse = Warehouse()
    validator = Validator()
    warehouse_manager = WarehouseManager(catalog, validator, warehouse)
    loose_material_manager = LooseMaterialManager(catalog, validator)
    menu = Menu(catalog, warehouse, warehouse_manager, validator, loose_material_manager)
    while True:
        output = menu.display_menu()
        if output == "0":
            menu.get_user_choice(output)
            break
        menu.get_user_choice(output)
