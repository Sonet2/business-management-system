import os, json
class Wood_Catalog:
    def __init__(self, wood_catalog_file = "prices.json"):
        self.catalog = {}
        self.load_catalog(wood_catalog_file)

    def load_catalog(self, wood_catalog_file):
        try: 
            with open(wood_catalog_file, "r") as wood_catalog:
                self.catalog = json.load(wood_catalog)
        except (FileNotFoundError, json.JSONDecodeError):
            self.catalog = {}

    def get_wood_category(self):
        return list(self.catalog.keys())
    
    def get_wood_subcategory(self,category):
        return list(self.catalog[category].keys())
    
    def get_wood_specie(self, category, subcategory):
        return list(self.catalog[category][subcategory].keys())
    
    def get_wood_price(self, category, subcategory, specie):
        return self.catalog[category][subcategory][specie]
    