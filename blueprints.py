from wood_catalog import WoodCatalog
from validators import Validator
class Blueprints:
    def __init__(self, validator, catalog):
        self.validator = validator
        self.catalog = catalog

    def enumerate_order_items(self, item_list):
            for index, item in enumerate(item_list, start=1):
                print(f"{index}. {item}")
                
    def wood_selection(self):
        wood_category = self.catalog.get_wood_category()
        selected_category = self.validator.select_option_from_list(wood_category, "Wybierz kategorię drewna (numer): ")

        wood_subcategory = self.catalog.get_wood_subcategory(selected_category)
        if wood_subcategory is None:
            selected_subcategory = None
        else:
            selected_subcategory = self.validator.select_option_from_list(wood_subcategory, "Wybierz podkategorię drewna (numer): ")
        
        wood_species = self.catalog.get_wood_specie(selected_category, selected_subcategory)
        if wood_species is None:
            selected_specie = None
        else:
            selected_specie = self.validator.select_option_from_list(wood_species, "Wybierz gatunek drewna (numer): ")

        wood_price = self.catalog.get_wood_price(selected_category, selected_subcategory, selected_specie)
        if not wood_price:
            raise ValueError("Nie znaleziono ceny dla wybranego gatunku drewna.")
        wood_price = wood_price[0] 

        m3_quantity = self.validator.get_valid_number("Podaj ilość w m3: ", float, 0.01)
        length = self.validator.get_valid_number("Podaj długość w metrach: ", float, 0.01)
        dimensions = input("Podaj wymiary (np. 10x20): ").strip()
        while not dimensions:
            print("Wymiary nie mogą być puste.")
            dimensions = input("Podaj wymiary (np. 10x20): ").strip()

        return selected_category, selected_subcategory, selected_specie, wood_price, m3_quantity, length, dimensions

    