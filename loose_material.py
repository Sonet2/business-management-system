import json
import wood_catalog, warehouse_management

class Material:
    def __init__(self, prices_file="prices.json"):
        self.prices_file = prices_file
        self.prices_data = self.load_prices_data()
    
    def load_prices_data(self):
        try:
            with open(self.prices_file, "r") as prices_file:
                data = json.load(prices_file)
        except FileNotFoundError:
            print(f"Plik {self.prices_file} nie został znaleziony. Inicjalizacja pustego cennika.")
            data = {}
        except json.JSONDecodeError:
            print(f"Błąd dekodowania JSON w pliku {self.prices_file}. Inicjalizacja pustego cennika.")
            data = {}
        return data
    
    def calculate_price(self, category, subcategory, wood_specie, m3, length, piece_dimensions):
        price_per_m3 = self.get_wood_price(category, subcategory, wood_specie)
        if price_per_m3 is None:
            print("Nie znaleziono ceny dla wybranego gatunku drewna.")
            return None
        final_price = m3 * price_per_m3
        return {
            "typ": category,
            "podkategoria": subcategory,
            "gatunek": wood_specie,
            "m3": m3,
            "dlugosc": length,
            "wymiary_sztuki": piece_dimensions,
            "cena": final_price
        }
            