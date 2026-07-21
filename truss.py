import json, math
class WoodMaterial:
    def __init__(self, name, length, height, width, quantity, price_per_m3):
        self.name = name
        self.length = length
        self.height = height
        self.width = width
        self.quantity = quantity
        self.price_per_m3 = price_per_m3

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
    
    def set_krokiew(self, material: WoodMaterial):
        self.krokiew = material

    def set_murlata(self, material: WoodMaterial):
        self.murlata = material

    def set_jetka(self, material: WoodMaterial):
        self.jetka = material
    
    def set_lata(self, width: float, height: float, laty_spacing: float, price_per_m3: float):
        if self.krokiew is None:
            raise ValueError("Najpierw wprowadź krokiew, aby obliczyć łaty!")
    
        laty_length = (self.spacing / 100) * (self.krokiew.quantity - 2)
        quantity = self.krokiew.length / (laty_spacing / 100)

        self.lata = WoodMaterial("Łaty", laty_length, height, width, quantity, price_per_m3)
        

    def set_kontrlata(self, width: float, height: float, price_per_m3: float):
        if self.krokiew is None:
            raise ValueError("Najpierw wprowadź krokiew, aby obliczyć kontrłaty!")
        
        kontrlaty_length = self.krokiew.length
        quantity = self.krokiew.quantity
        self.kontrlata = WoodMaterial("Kontrłaty", kontrlaty_length, height, width, quantity, price_per_m3)
        
    def set_platew(self, material: WoodMaterial):
        self.platew = material
    
    def set_slup(self, material: WoodMaterial):
        self.slup = material


class TrussManager:
    def __init__(self, validator):
        self.validator = validator
    
    def create_truss(self, spacing):
        if not self.validator.get_positive_float(spacing):
            raise ValueError("Rozstaw krokwi musi być większy od zera.")
        return Truss(spacing)
