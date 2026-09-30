from database import Database 
from wood_catalog import WoodCatalog

class Warehouse:
    def __init__(self, connection, catalog):
        self.connection = connection
        self.catalog = catalog

    def _fetch_flat_list(self, query, params=()):
            rows = self.connection.execute(query,params).fetchall()
            return[row[0] for row in rows]
    
    
    def write_to_warehouse(self, category, subcategory, wood_specie, m3, dimensions, length):
        material_id = self.catalog.get_position_id(category, subcategory, wood_specie)

        if not material_id or material_id == [None]:
            print("Nie znaleziono materiału w katalogu drewna.")
            return
        
        
        result = self.connection.execute("""
            INSERT INTO warehouse (material_id, m3_quantity, dimensions, length)
            VALUES (?, ?, ?, ?)
        """, (material_id[0], m3, dimensions, length))

        self.connection.commit()

        if result.rowcount > 0:
            print("Materiał został dodany do magazynu.")

    
    def delete_material(self, id_to_delete: int):
        result = self.connection.execute("DELETE FROM warehouse WHERE id = ?", (id_to_delete,))
        self.connection.commit()
        if result.rowcount > 0:
            return True
        else:
            return False

    def display_warehouse(self):
        results = self.connection.execute("SELECT warehouse.id, materials.category, materials.subcategory, wood_species.name, m3_quantity, dimensions, length FROM warehouse INNER JOIN materials ON warehouse.material_id = materials.id LEFT JOIN wood_species ON materials.wood_species_id = wood_species.id")
        for entry in results:
            if entry[2] is None:
                print(f"ID: {entry[0]}, Kategoria: {entry[1]}, Podkategoria: brak, Gatunek: {entry[3]}, Ilość m3: {entry[4]}, Wymiary sztuki: {entry[5]}, Długość: {entry[6]}")
            elif entry[3] is None:
                print(f"ID: {entry[0]}, Kategoria: {entry[1]}, Podkategoria: brak, Gatunek: brak, Ilość m3: {entry[4]}, Wymiary sztuki: {entry[5]}, Długość: {entry[6]}")
            else:
                print(f"ID: {entry[0]}, Kategoria: {entry[1]}, Podkategoria: {entry[2]}, Gatunek: {entry[3]}, Ilość m3: {entry[4]}, Wymiary sztuki: {entry[5]}, Długość: {entry[6]}") 


class WarehouseManager:
    def __init__(self, catalog, validator, warehouse):
        self.catalog = catalog
        self.validator = validator
        self.warehouse = warehouse
    
    def add_to_warehouse(self):
        category = self.validator.select_option_from_list(self.catalog.get_wood_category(), "Wybierz kategorię drewna: ")
        subcategory_options = self.catalog.get_wood_subcategory(category)
        if subcategory_options is None:
            subcategory = None
        elif not subcategory_options:
            raise Exception(f"Błąd: Brak podkategorii dla wybranej kategorii: {category}")
        else:
            subcategory = self.validator.select_option_from_list(subcategory_options, "Wybierz podkategorię drewna: ")

        wood_specie_options = self.catalog.get_wood_specie(category, subcategory)
        if wood_specie_options is None:
            wood_specie = None
        elif not wood_specie_options:
            raise Exception(f"Błąd: Brak gatunku drewna dla wybranej kategorii: {category} i podkategorii: {subcategory}")
        else:
            wood_specie = self.validator.select_option_from_list(wood_specie_options, "Wybierz gatunek drewna: ")
            
            
        m3 = self.validator.get_valid_number("Wprowadź ilość w m3: ", float, 0.0001)

        dimensions = input("Wprowadź wymiary sztuki: ")        
        while not dimensions:            
            print("Wymiary sztuki nie mogą być puste.")            
            dimensions = input("Wprowadź wymiary sztuki: ")

        length = self.validator.get_valid_number("Wprowadź długość drewna: ", float, 0.0001)

        self.warehouse.write_to_warehouse(category, subcategory, wood_specie, m3, dimensions, length)
    

    def delete_from_warehouse(self):
        self.warehouse.display_warehouse()
            
        id_to_delete = self.validator.get_valid_number("Wprowadź ID materiału do usunięcia: ", int, 1)
        
        if self.warehouse.delete_material(id_to_delete):
            print(f"Materiał o ID {id_to_delete} został usunięty.")
        else:
            print(f"Nie znaleziono materiału o ID {id_to_delete}.")