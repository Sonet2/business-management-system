import math
from base_repository import BaseOrderRepository
from order import OrderBlueprint
class TrussMaterial:

    def __init__(self, name, wood_specie, length, height, width, quantity, price_per_m3):
        self.name = name
        self.wood_specie = wood_specie
        self.length = length
        self.height = height
        self.width = width
        self.quantity = quantity
        self.price_per_m3 = price_per_m3

    def to_dict(self):
        return {
            "nazwa": self.name,
            "gatunek": self.wood_specie,
            "dlugosc": self.length,
            "wysokosc": self.height,
            "szerokosc": self.width,
            "ilosc": self.quantity,
            "cena_za_m3": self.price_per_m3,
            "calkowity_metraz_materialu": self.total_volume,
            "cena_calkowita_materialu": self.total_price
        }
    @classmethod
    def from_dict(cls, data):
        name = data.get("nazwa")
        wood_specie = data.get("gatunek")
        length = data.get("dlugosc")
        height = data.get("wysokosc")
        width = data.get("szerokosc")
        quantity = data.get("ilosc")
        price_per_m3 = data.get("cena_za_m3")
        return cls(name, wood_specie, length, height, width, quantity, price_per_m3)

    @property
    def total_volume(self):
        return self.length * (self.height/100) * (self.width/100) * self.quantity
    
    @property
    def total_price(self):
        return self.total_volume * self.price_per_m3
    
class Truss:
    def __init__(self, spacing):
        self.spacing = spacing
        self.krokiew = None
        self.murlata = None
        self.jetka = None
        self.lata = None
        self.kontrlata = None
        self.platew = None
        self.slup = None

    @property
    def total_volume(self):
        total_volume = 0
        for component in [self.krokiew, self.murlata, self.jetka, self.lata, self.kontrlata, self.platew, self.slup]:
            if component is not None:
                total_volume += component.total_volume
        return total_volume
    
    @property
    def total_price(self):
        total_price = 0
        for component in [self.krokiew, self.murlata, self.jetka, self.lata, self.kontrlata, self.platew, self.slup]:
            if component is not None:
                total_price += component.total_price
        return total_price
    
    def to_dict(self):
        return {
            "rozstaw_krokwi": self.spacing,
            "krokiew": self.krokiew.to_dict() if self.krokiew else None,
            "murlata": self.murlata.to_dict() if self.murlata else None,
            "jetka": self.jetka.to_dict() if self.jetka else None,
            "laty": self.lata.to_dict() if self.lata else None,
            "kontrlaty": self.kontrlata.to_dict() if self.kontrlata else None,
            "platew": self.platew.to_dict() if self.platew else None,
            "slup": self.slup.to_dict() if self.slup else None,
            "calkowity_metraz_zamowienia": self.total_volume,
            "calkowita_cena_zamowienia": self.total_price
        }
    @classmethod
    def from_dict(cls, data):
        spacing = data.get("rozstaw_krokwi")
        truss = cls(spacing)
        truss.krokiew = TrussMaterial.from_dict(data.get("krokiew")) if data.get("krokiew") else None
        truss.murlata = TrussMaterial.from_dict(data.get("murlata")) if data.get("murlata") else None
        truss.jetka = TrussMaterial.from_dict(data.get("jetka")) if data.get("jetka") else None
        truss.lata = TrussMaterial.from_dict(data.get("laty")) if data.get("laty") else None
        truss.kontrlata = TrussMaterial.from_dict(data.get("kontrlaty")) if data.get("kontrlaty") else None
        truss.platew = TrussMaterial.from_dict(data.get("platew")) if data.get("platew") else None
        truss.slup = TrussMaterial.from_dict(data.get("slup")) if data.get("slup") else None
        return truss
    
    def set_krokiew(self, material: TrussMaterial):
        self.krokiew = material

    def set_murlata(self, material: TrussMaterial):
        self.murlata = material

    def set_jetka(self, material: TrussMaterial):
        self.jetka = material
    
    def set_lata(self, width: float, height: float, laty_spacing: float, price_per_m3: float):
        if self.krokiew is None:
            raise ValueError("Najpierw wprowadź krokiew, aby obliczyć łaty!")
    
        laty_length = math.ceil((self.spacing / 100) * (self.krokiew.quantity - 2))
        quantity = math.ceil(self.krokiew.length / (laty_spacing / 100))

        self.lata = TrussMaterial("Łaty", None, laty_length, height, width, quantity, price_per_m3)
        

    def set_kontrlata(self, width: float, height: float, price_per_m3: float):
        if self.krokiew is None:
            raise ValueError("Najpierw wprowadź krokiew, aby obliczyć kontrłaty!")
        
        kontrlaty_length = self.krokiew.length
        quantity = self.krokiew.quantity

        self.kontrlata = TrussMaterial("Kontrłaty", None, kontrlaty_length, height, width, quantity, price_per_m3)

    def set_platew(self, material: TrussMaterial):
        self.platew = material
    
    def set_slup(self, material: TrussMaterial):
        self.slup = material

class TrussOrderBlueprint(OrderBlueprint):
    material_class = Truss
    
class TrussOrder(BaseOrderRepository):
    def __init__(self, order_file = "truss_orders.json"):
        super().__init__(order_file, TrussOrderBlueprint)


class TrussManager:
    def __init__(self, validator, catalog):
        self.validator = validator
        self.wood_catalog = catalog

    def get_material_inputs(self, name: str, category: str):
        length = self.validator.get_positive_float(f"Podaj długość {name} w metrach: ")
        height = self.validator.get_positive_float(f"Podaj wysokość {name} w centymetrach: ")
        width = self.validator.get_positive_float(f"Podaj szerokość {name} w centymetrach: ")
        quantity = self.validator.get_valid_number(f"Podaj ilość {name}: ", int, 1)
        wood_specie = self.validator.select_option_from_list(self.wood_catalog.get_wood_specie(category, None), f"Wybierz gatunek drewna dla {name}: ")
        price_per_m3 = self.wood_catalog.get_wood_price(category, None, wood_specie)
        
        material = TrussMaterial(name, wood_specie, length, height, width, quantity, price_per_m3)
        return material
    
    def add_krokiew(self, truss: Truss):
        krokiew_material = self.get_material_inputs("Krokiew", "Kantówka")
        truss.set_krokiew(krokiew_material)


    def add_murlata(self, truss: Truss):
        murlata_material = self.get_material_inputs("Murlata", "Belka")
        truss.set_murlata(murlata_material)
        
    def add_jetka(self, truss: Truss):
        jetka_material = self.get_material_inputs("Jetka", "Kantówka")
        truss.set_jetka(jetka_material)
    
    def add_platew(self, truss: Truss):
        platew_material = self.get_material_inputs("Płatwie", "Belka")
        truss.set_platew(platew_material)

    def add_slup(self, truss: Truss):
        slup_material = self.get_material_inputs("Słup", "Belka")
        truss.set_slup(slup_material)
    
    def add_lata(self, truss: Truss):

        laty_spacing = self.validator.get_positive_float("Podaj rozstaw łat w centymetrach: ")
        width = self.validator.get_positive_float("Podaj szerokość łat w centymetrach: ")
        height = self.validator.get_positive_float("Podaj wysokość łat w centymetrach: ")
        price_per_m3 = self.wood_catalog.get_wood_price("Łaty", None, None)
        
        truss.set_lata(width, height, laty_spacing, price_per_m3)

    def add_kontrlata(self, truss: Truss):
        width = self.validator.get_positive_float("Podaj szerokość kontrłat w centymetrach: ")
        height = self.validator.get_positive_float("Podaj wysokość kontrłat w centymetrach: ")
        price_per_m3 = self.wood_catalog.get_wood_price("Kontrłaty", None, None)
        
        truss.set_kontrlata(width, height, price_per_m3)

    def collect_order(self):
        spacing = self.validator.get_positive_float("Podaj rozstaw krokwi w centymetrach: ")
        truss = Truss(spacing)
        self.add_krokiew(truss)
        self.add_murlata(truss)
        self.add_jetka(truss)
        self.add_lata(truss)
        self.add_kontrlata(truss)
        x = input("Czy chcesz dodać platwie i slupy? (tak/nie): ").strip().lower()
        if x == "tak":
            self.add_platew(truss)
            self.add_slup(truss)    
        return truss
        