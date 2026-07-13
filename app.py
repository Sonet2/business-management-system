import warehouse_management, wood_catalog
class Menu:
    def __init__(self, catalog, warehouse):
        self.catalog = catalog
        self.warehouse = warehouse
        

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
        choice = int(input(qst))
        
        while choice < 1 or choice > len(options):
            print("Nieprawidłowy wybór.")
            choice = int(input(qst))

        return options[choice - 1]
    
    def add_to_warehouse(self):
        category = self.select_option_from_list(self.catalog.get_wood_category(), "Wybierz kategorię drewna: ")
                
        if category == "Tarcica":
            subcategory = self.select_option_from_list(self.catalog.get_wood_subcategory(category), "Wybierz podkategorię drewna: ")
        else:
            subcategory = None
        
        if category == "Łaty" or category == "Kontrłaty":
            wood_specie = None
        else:
            wood_specie = self.select_option_from_list(self.catalog.get_wood_specie(category, subcategory), "Wybierz gatunek drewna: ")
        
        m3 = float(input("Wprowadź ilość w m3: "))
        while m3 <= 0:
            print("Ilość w m3 musi być liczbą dodatnią.")
            m3 = float(input("Wprowadź ilość w m3: "))

        length = float(input("Wprowadź długość drewna: "))
        while length <= 0:  
            print("Długość drewna musi być liczbą dodatnią.")
            length = float(input("Wprowadź długość drewna: "))

        piece_dimensions = input("Wprowadź wymiary sztuki: ")
        while not piece_dimensions:
            print("Wymiary sztuki nie mogą być puste.")
            piece_dimensions = input("Wprowadź wymiary sztuki: ")

        self.warehouse.write_to_warehouse(category, subcategory, wood_specie, m3, length, piece_dimensions)
    
    def display_warehouse(self):
        for entry in self.warehouse.warehouse_data:
            print(f"ID: {entry.id}, Kategoria: {entry.category}, Podkategoria: {entry.subcategory}, Gatunek: {entry.wood_specie}, Ilość m3: {entry.m3}, Długość: {entry.length}, Wymiary sztuki: {entry.piece_dimensions}")
    
    def delete_from_warehouse(self):
        self.display_warehouse()
        id_to_delete = int(input("Wprowadź ID materiału do usunięcia: "))
        
        while id_to_delete <= 0:
            print("ID musi być liczbą dodatnią.")
            id_to_delete = int(input("Wprowadź ID materiału do usunięcia: "))
        
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
                self.display_warehouse()
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
    warehouse = warehouse_management.Warehouse()
    catalog = wood_catalog.Wood_Catalog()
    menu = Menu(catalog, warehouse)
    while True:
        output = menu.display_menu()
        if output == "0":
            menu.get_user_choice(output)
            break
        menu.get_user_choice(output)