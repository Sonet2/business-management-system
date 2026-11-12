from database import Database 
from wood_catalog import WoodCatalog
import sqlite3

class Warehouse:
    def __init__(self, connection, catalog):
        self.connection = connection
        self.catalog = catalog
    
    def warehouse_insertion(self, material_id, m3_quantity, dimensions, length):
        
        try:
            result = self.connection.execute("""
                INSERT INTO warehouse (material_id, m3_quantity, dimensions, length)
                VALUES (?, ?, ?, ?)""", (material_id[0], m3_quantity, dimensions, length))
            self.connection.commit()
        except sqlite3.IntegrityError:
            self.connection.rollback()
            raise Exception(f"Nie można dodać materiału do magazynu. Sprawdź, czy materiał istnieje w katalogu.")
        
        if result.rowcount > 0:
            return result.lastrowid
        else:
            raise Exception("Nie udało się dodać materiału do bazy danych")
    
    def write_to_warehouse(self, category, subcategory, wood_specie, m3, dimensions, length):
        material_id = self.catalog.get_position_id(category, subcategory, wood_specie)
                
        if not material_id or material_id == [None]:
            raise Exception("Nie znaleziono materiału w katalogu. Nie można dodać do magazynu.")
            return

        result = self.warehouse_insertion(material_id, m3, dimensions, length)

        if result:
            print("Materiał został poprawnie dodany do magazynu.")

    
    def delete_material(self, id_to_delete: int):
        result = self.connection.execute("DELETE FROM warehouse WHERE id = ?", (id_to_delete,))
        self.connection.commit()
        if result.rowcount > 0:
            return True
        else:
            return False
    def get_warehouse(self):
        result = self.connection.execute("""
                SELECT warehouse.id, materials.category, materials.subcategory, wood_species.name, warehouse.m3_quantity, warehouse.dimensions, warehouse.length
                FROM warehouse 
                INNER JOIN materials ON warehouse.material_id = materials.id 
                LEFT JOIN wood_species ON materials.wood_species_id = wood_species.id
                """)
        results = []
        for entry in result:
            results.append(entry)
        return results
    
    def display_warehouse(self):
        results = self.get_warehouse()

        for entry in results:
            subcategory = entry[2]
            specie = entry[3]

            if subcategory is None:
                subcategory = "brak"

            if specie is None:
                specie = "brak"

            print(
                f"ID: {entry[0]}, Kategoria: {entry[1]}, "
                f"Podkategoria: {subcategory}, Gatunek: {specie}, "
                f"Ilość m3: {entry[4]}, Wymiary sztuki: {entry[5]}, "
                f"Długość: {entry[6]}"
            )

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

        dimensions = input("Wprowadź wymiary sztuki: ").strip()        
        while not dimensions:            
            print("Wymiary sztuki nie mogą być puste.")            
            dimensions = input("Wprowadź wymiary sztuki: ").strip()

        length = self.validator.get_valid_number("Wprowadź długość drewna: ", float, 0.0001)

        self.warehouse.write_to_warehouse(category, subcategory, wood_specie, m3, dimensions, length)
    

    def delete_from_warehouse(self):
        self.warehouse.display_warehouse()
            
        id_to_delete = self.validator.get_valid_number("Wprowadź ID materiału do usunięcia: ", int, 1)
        
        if self.warehouse.delete_material(id_to_delete):
            print(f"Materiał o ID {id_to_delete} został usunięty.")
        else:
            print(f"Nie znaleziono materiału o ID {id_to_delete}.")