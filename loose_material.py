class Material:
    def __init__(self, category, subcategory, wood_specie, m3, price_per_m3, length, piece_dimensions):
        self.category = category
        self.subcategory = subcategory
        self.wood_specie = wood_specie
        self.m3 = m3
        self.price_per_m3 = price_per_m3
        self.length = length
        self.piece_dimensions = piece_dimensions

    @property
    def total_price(self):
        return self.m3 * self.price_per_m3
    
    def to_dict(self):
        return {
            "typ": self.category,
            "podkategoria": self.subcategory,
            "gatunek": self.wood_specie,
            "m3": self.m3,
            "cena_za_m3": self.price_per_m3,
            "dlugosc": self.length,
            "wymiary_sztuki": self.piece_dimensions,
            "cena_laczna" : self.total_price
        }

class LooseMaterialOrder:
    def __init__(self):
        self.entries = []
    @property
    def total_price(self):
        return sum(entry.total_price for entry in self.entries)
    @property
    def total_m3(self):
        return sum(entry.m3 for entry in self.entries)
    
    def add_entry(self, category, subcategory, wood_specie, m3, price_per_m3, length, piece_dimensions):
        entry = Material(category, subcategory, wood_specie, m3, price_per_m3, length, piece_dimensions)
        self.entries.append(entry)
    def to_dict(self):
        return {
            "laczny_metraz": self.total_m3,
            "laczna_cena": self.total_price,
            "pozycje": [entry.to_dict() for entry in self.entries]
        }

class LooseMaterialManager:
    def __init__(self, catalog, validator):
        self.catalog = catalog
        self.validator = validator

    def collect_order(self):
        order = LooseMaterialOrder()
        while True:
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

            price_per_m3 = self.catalog.get_wood_price(category, subcategory, wood_specie)

            length = self.validator.get_valid_number("Wprowadź długość drewna: ", float, 0.0001)

            piece_dimensions = input("Wprowadź wymiary sztuki: ")        
            while not piece_dimensions:            
                print("Wymiary sztuki nie mogą być puste.")            
                piece_dimensions = input("Wprowadź wymiary sztuki: ")
            
            order.add_entry(category, subcategory, wood_specie, m3, price_per_m3, length, piece_dimensions)
            
            continue_order = input("Czy chcesz dodać kolejny materiał? (tak/nie): ").strip().lower()
            if continue_order != "tak":
                break

        return order.to_dict()
