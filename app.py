import warehouse_management, wood_catalog
class Menu:
    def __init__(self):
        pass

    def display_menu(self):
        print("Wybierz opcję:")
        print("1. Obsługa Magazynu")
        print("2. Zamówienie dla klienta")
        output = input("Wprowadź numer opcji: ")
        return output
    
    def get_user_choice(self, output):
        self.output = output
        if output == "1":
            print("Wybrano opcję 1: Obsługa Magazynu")
            print("Wybierz działanie:")
            print("1. Dodaj materiał do magazynu")
            print("2. Usuń materiał z magazynu")
            print("3. Wyświetl zawartość magazynu")
            warehouse_option = input("Wprowadź numer opcji: ")
            catalog = wood_catalog.Wood_Catalog()
            
            if warehouse_option == "1":
                categories = catalog.get_wood_category()
                for i, cat in enumerate(categories, start=1):
                    print(f"{i}. {cat}")
                category_choice = int(input("Wybierz kategorię drewna: "))
                category = categories[category_choice - 1]


                if category == "Tarcica":
                    subcategories = catalog.get_wood_subcategory(category)
                    for i, sub in enumerate(subcategories, start=1):
                        print(f"{i}. {sub}")
                    subcategory_choice = int(input("Wybierz podkategorię drewna: "))
                    subcategory = subcategories[subcategory_choice - 1]
                else:
                    subcategory = None
                
                species = catalog.get_wood_specie(category, subcategory)
                for i, sp in enumerate(species, start=1):
                    print(f"{i}. {sp}")
                specie_choice = int(input("Wybierz gatunek drewna: "))
                wood_specie = species[specie_choice - 1]

                m3 = float(input("Wprowadź ilość w m3: "))
                length = float(input("Wprowadź długość drewna: "))
                piece_dimensions = input("Wprowadź wymiary sztuki: ")
                warehouse = warehouse_management.Warehouse()
                warehouse.write_to_warehouse(category, subcategory, wood_specie, m3, length, piece_dimensions)
            
            elif warehouse_option == "2":
                warehouse = warehouse_management.Warehouse()
                for entry in warehouse.warehouse_data:
                    print(f"ID: {entry['id']}\n Typ: {entry['typ']}\n Podkategoria: {entry['podkategoria']}\n Gatunek: {entry['gatunek']}\n Ilość m3: {entry['m3']}\n Długość: {entry['dlugosc']}\n Wymiary sztuki: {entry['wymiary_sztuki']}\n")
                id_to_delete = int(input("Wprowadź ID materiału do usunięcia: "))
                if warehouse.delete_material(id_to_delete):
                    print(f"Materiał o ID {id_to_delete} został usunięty.")
                else:
                    print(f"Nie znaleziono materiału o ID {id_to_delete}.")
            
            else:
                warehouse = warehouse_management.Warehouse()
                for entry in warehouse.warehouse_data:
                    print(f"ID: {entry['id']}\n Typ: {entry['typ']}\n Podkategoria: {entry['podkategoria']}\n Gatunek: {entry['gatunek']}\n Ilość m3: {entry['m3']}\n Długość: {entry['dlugosc']}\n Wymiary sztuki: {entry['wymiary_sztuki']}\n")
        elif output == "2":
            pass

if __name__ == "__main__":
    menu = Menu()
    output = menu.display_menu()
    menu.get_user_choice(output)