import json
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
        if category == "Tarcica":
            return list(self.catalog[category].keys())
        else:
            return None
    
    def get_wood_specie(self, category, subcategory):
        if subcategory is None:
            return list(self.catalog[category].keys())
        else:
            return list(self.catalog[category][subcategory].keys())
    
    def get_wood_price(self, category, subcategory, specie):
        if subcategory is None:
            return self.catalog[category][specie]
        else:
            return self.catalog[category][subcategory][specie]
    