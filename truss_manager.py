from truss import Truss, TrussMaterial

class TrussManager:
    def __init__(self, validator, catalog):
        self.validator = validator
        self.catalog = catalog

    def get_material_inputs(self, name: str, category: str,minimum : int = 1, multiple_of: int = 1):
        wood_specie = self.validator.select_option_from_list(self.catalog.get_wood_specie(category, None), f"Wybierz gatunek drewna dla {name}: ")
        length = self.validator.get_positive_float(f"Podaj długość {name} w metrach: ")
        height = self.validator.get_positive_float(f"Podaj wysokość {name} w centymetrach: ")
        width = self.validator.get_positive_float(f"Podaj szerokość {name} w centymetrach: ")
        quantity = self.validator.get_valid_number(f"Podaj ilość {name}: ", int, minimum, multiple_of=multiple_of)
        return TrussMaterial(name, category, wood_specie, length, height, width, quantity)

    def add_krokiew(self, truss: Truss):
        krokiew_material = self.get_material_inputs("Krokiew", "kantowka", minimum=4, multiple_of=2)
        truss.set_krokiew(krokiew_material)


    def add_murlata(self, truss: Truss):
        murlata_material = self.get_material_inputs("Murlata", "belka")
        truss.set_murlata(murlata_material)
        
    def add_jetka(self, truss: Truss):
        jetka_material = self.get_material_inputs("Jetka", "kantowka")
        truss.set_jetka(jetka_material)
    
    def add_platew(self, truss: Truss):
        platew_material = self.get_material_inputs("Płatwie", "belka")
        truss.set_platew(platew_material)

    def add_slup(self, truss: Truss):
        slup_material = self.get_material_inputs("Słup", "belka")
        truss.set_slup(slup_material)

    def add_lata(self, truss: Truss):

        laty_spacing = self.validator.get_positive_float("Podaj rozstaw łat w centymetrach: ")
        width = self.validator.get_positive_float("Podaj szerokość łat w centymetrach: ")
        height = self.validator.get_positive_float("Podaj wysokość łat w centymetrach: ")
        
        truss.set_lata(width, height, laty_spacing)

    def add_kontrlata(self, truss: Truss):
        width = self.validator.get_positive_float("Podaj szerokość kontrłat w centymetrach: ")
        height = self.validator.get_positive_float("Podaj wysokość kontrłat w centymetrach: ")
        
        truss.set_kontrlata(width, height)

    def collect_truss(self):
        spacing = self.validator.get_positive_float("Podaj rozstaw krokwi w centymetrach: ")
        truss = Truss(spacing)
        self.add_krokiew(truss)
        self.add_murlata(truss)
        self.add_jetka(truss)
        self.add_lata(truss)
        self.add_kontrlata(truss)
        choice = self.validator.select_option_from_list(["tak", "nie"], "Czy chcesz dodać płatwie i słupy? ")
        if choice == "tak":
            self.add_platew(truss)
            self.add_slup(truss)    
        return truss

    def build_items(self, truss: Truss):
        items = []
        for component in truss.components:
            price_per_m3 = self.catalog.get_wood_price(component.category, None, component.wood_specie)
            if not price_per_m3:
                raise Exception(f"Nie znaleziono ceny dla materiału: {component.name}, gatunek drewna: {component.wood_specie}")
            dimensions = f"{component.width:g}x{component.height:g}"
            m3_quantity = component.total_volume
            items.append((component.category, None, component.wood_specie, price_per_m3[0], m3_quantity, component.length, dimensions))
        return items
