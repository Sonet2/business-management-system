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
            if entry.category == category and entry.subcategory == subcategory and entry.wood_specie == wood_specie and entry.length == length and entry.piece_dimensions == piece_dimensions:
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
