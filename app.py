from warehouse_management import Warehouse
from wood_catalog import WoodCatalog
from validators import Validator

class Menu:
    def __init__(self, catalog, warehouse, validator):
        self.catalog = catalog
        self.warehouse = warehouse
        self.validator = validator
        

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
            pass
        elif output == "0":
            print("Zamknięcie programu.")
        else:
            print("Nieprawidłowa opcja. Spróbuj ponownie.")
    
    def select_option_from_list(self, options: list[str], qst: str) -> str:
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

        choice = self.validator.get_valid_number(qst, int, 1, len(options))
        return options[choice - 1]
    
    
    def add_to_warehouse(self):
        category = self.select_option_from_list(self.catalog.get_wood_category(), "Wybierz kategorię drewna: ")
        subcategory_options = self.catalog.get_wood_subcategory(category)
        if not subcategory_options:
            subcategory = None
        else:
            subcategory = self.select_option_from_list(subcategory_options, "Wybierz podkategorię drewna: ")
        
        if category == "Łaty" or category == "Kontrłaty":
            wood_specie = None
        else:
            wood_specie = self.select_option_from_list(self.catalog.get_wood_specie(category, subcategory), "Wybierz gatunek drewna: ")
        
        m3 = self.validator.get_valid_number("Wprowadź ilość w m3: ", float, 0.0001)

        length = self.validator.get_valid_number("Wprowadź długość drewna: ", float, 0.0001)

        piece_dimensions = input("Wprowadź wymiary sztuki: ")        
        while not piece_dimensions:            
            print("Wymiary sztuki nie mogą być puste.")            
            piece_dimensions = input("Wprowadź wymiary sztuki: ")

        self.warehouse.write_to_warehouse(category, subcategory, wood_specie, m3, length, piece_dimensions)
    
   
    def delete_from_warehouse(self):
        self.warehouse.display_warehouse()
        
        id_to_delete = self.validator.get_valid_number("Wprowadź ID materiału do usunięcia: ", int, 1, self.warehouse.get_max_id())
        
        if self.warehouse.delete_material(id_to_delete):
            print(f"Materiał o ID {id_to_delete} został usunięty.")
        else:
            print(f"Nie znaleziono materiału o ID {id_to_delete}.")
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
                self.add_to_warehouse()
            elif warehouse_option == "2":
                self.delete_from_warehouse()
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
            pass
        elif order_option == "2":
            pass
        else:
            print("Nieprawidłowa opcja. Spróbuj ponownie.")

if __name__ == "__main__":
    warehouse = Warehouse()
    catalog = WoodCatalog()
    validator = Validator()
    menu = Menu(catalog, warehouse, validator)
    while True:
        output = menu.display_menu()
        if output == "0":
            menu.get_user_choice(output)
            break
        menu.get_user_choice(output)