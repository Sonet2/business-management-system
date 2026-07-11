import json

class Warehouse:
    def __init__(self, warehouse_file="warehouse.json"):
        self.warehouse_file = warehouse_file
        self.warehouse_data = self.load_warehouse_data()
    
        
    def load_warehouse_data(self):
        try:
            with open(self.warehouse_file, "r") as warehouse_file:
                data = list(json.load(warehouse_file))
        except FileNotFoundError:
            data = []
        except json.JSONDecodeError:
            print(f"Błąd dekodowania JSON w pliku {self.warehouse_file}. Inicjalizacja pustego magazynu.")
            data = []
        return data

    

    def write_to_warehouse(self, category, subcategory, wood_specie, m3, length, piece_dimensions):
        
        for entry in self.warehouse_data:
            if entry["typ"] == category and entry["podkategoria"] == subcategory and entry["gatunek"] == wood_specie and entry["dlugosc"] == length and entry["wymiary_sztuki"] == piece_dimensions:
                entry["m3"] += m3
                try: 
                    with open(self.warehouse_file, "w") as warehouse_file:
                        json.dump(self.warehouse_data, warehouse_file, ensure_ascii=False, indent=4)
                except OSError as e:
                    print(f"Wystąpił błąd podczas zapisywania danych do pliku: {e}")
                return
            
        new_entry = {
            "id" : max([entry["id"] for entry in self.warehouse_data], default=0) + 1,
            "typ": category,
            "podkategoria": subcategory,
            "gatunek": wood_specie,
            "m3": m3,
            "dlugosc": length,
            "wymiary_sztuki": piece_dimensions
        }
        self.warehouse_data.append(new_entry)
        try: 
            with open(self.warehouse_file, "w") as warehouse_file:
                json.dump(self.warehouse_data, warehouse_file, ensure_ascii=False, indent=4)
        except OSError as e:
            print(f"Wystąpił błąd podczas zapisywania danych do pliku: {e}")
        return

    
    def delete_material(self, id_to_delete: int):
        for entry in self.warehouse_data:
            if entry["id"] == id_to_delete:
                self.warehouse_data.remove(entry)
                try:
                    with open(self.warehouse_file, "w") as warehouse_file:
                        json.dump(self.warehouse_data, warehouse_file, ensure_ascii=False, indent=4)
                except OSError as e:
                    print(f"Wystąpił błąd podczas usuwania danych: {e}")
                return True
                
        return False
    
if __name__ == "__main__":
    warehouse = Warehouse()
    warehouse.write_to_warehouse("Deska", None, "Modrzew", 5, 2.5, "2.5")
    print(warehouse.warehouse_data)