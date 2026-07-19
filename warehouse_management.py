import json

class MaterialEntry:
    def __init__(self, id, category, subcategory, wood_specie, m3, length, piece_dimensions):
        self.id = id
        self.category = category
        self.subcategory = subcategory
        self.wood_specie = wood_specie
        self.m3 = m3
        self.length = length
        self.piece_dimensions = piece_dimensions

    def to_dict(self):
        return {
            "id": self.id,
            "typ": self.category,
            "podkategoria": self.subcategory,
            "gatunek": self.wood_specie,
            "m3": self.m3,
            "dlugosc": self.length,
            "wymiary_sztuki": self.piece_dimensions
        }
    def matches(self, category, subcategory, wood_specie, length, piece_dimensions):
        if self.category == category and self.subcategory == subcategory and self.wood_specie == wood_specie and self.length == length and self.piece_dimensions == piece_dimensions:
            return True
        return False

class Warehouse:
    def __init__(self, warehouse_file="warehouse.json"):
        self.warehouse_file = warehouse_file
        self.warehouse_data = self.load_warehouse_data()

    def load_warehouse_data(self):
        try:
            with open(self.warehouse_file, "r") as warehouse_file:
                data = list(json.load(warehouse_file))
                entries = []
                for raw_entry in data:
                    entry = MaterialEntry(raw_entry["id"], raw_entry["typ"], raw_entry["podkategoria"], raw_entry["gatunek"], raw_entry["m3"], raw_entry["dlugosc"], raw_entry["wymiary_sztuki"])
                    entries.append(entry)
        except FileNotFoundError:
            entries = []
        except json.JSONDecodeError:
            print(f"Błąd dekodowania JSON w pliku {self.warehouse_file}. Inicjalizacja pustego magazynu.")
            entries = []
        return entries

    def save_data_check(self):
        try:
            with open(self.warehouse_file, "w") as warehouse_file:
                json.dump([entry.to_dict() for entry in self.warehouse_data], warehouse_file, ensure_ascii=False, indent=4)
        except OSError as e:
            print(f"Wystąpił błąd podczas zapisywania danych do pliku: {e}")

    def write_to_warehouse(self, category, subcategory, wood_specie, m3, length, piece_dimensions):
        
        for entry in self.warehouse_data:
            if entry.matches(category, subcategory, wood_specie, length, piece_dimensions):
                entry.m3 += m3
                self.save_data_check()
                return
            
        new_entry = MaterialEntry(
            id=max([e.id for e in self.warehouse_data], default=0) + 1,
            category = category,
            subcategory = subcategory,
            wood_specie = wood_specie,
            m3 = m3,
            length = length,
            piece_dimensions = piece_dimensions
        )
        self.warehouse_data.append(new_entry)
        self.save_data_check()
        return

    
    def delete_material(self, id_to_delete: int):
        for entry in self.warehouse_data:
            if entry.id == id_to_delete:
                self.warehouse_data.remove(entry)
                self.save_data_check()
                return True    
        return False
    
    def display_warehouse(self):
        for entry in self.warehouse_data:
            print(f"ID: {entry.id}, Kategoria: {entry.category}, Podkategoria: {entry.subcategory}, Gatunek: {entry.wood_specie}, Ilość m3: {entry.m3}, Długość: {entry.length}, Wymiary sztuki: {entry.piece_dimensions}")
    
    def get_max_id(self):
        if not self.warehouse_data:
            return 0
        return max(entry.id for entry in self.warehouse_data)
    


class WarehouseManager:
    def __init__(self, catalog, validator, warehouse):
        self.catalog = catalog
        self.validator = validator
        self.warehouse = warehouse
    
    def add_to_warehouse(self):
        category = self.validator.select_option_from_list(self.catalog.get_wood_category(), "Wybierz kategorię drewna: ")
        subcategory_options = self.catalog.get_wood_subcategory(category)
        if not subcategory_options:
            subcategory = None
        else:
            subcategory = self.validator.select_option_from_list(subcategory_options, "Wybierz podkategorię drewna: ")
        
        if category == "Łaty" or category == "Kontrłaty":
            wood_specie = None
        else:
            wood_specie = self.validator.select_option_from_list(self.catalog.get_wood_specie(category, subcategory), "Wybierz gatunek drewna: ")
        
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