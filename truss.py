import math
from dataclasses import dataclass
@dataclass
class TrussMaterial:
    name: str
    category: str
    wood_specie: str | None
    length: float
    height: float
    width: float
    quantity: int

    @property
    def total_volume(self):
        return self.length * (self.height/100) * (self.width/100) * self.quantity
    
    
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
        for component in self.components:
            total_volume += component.total_volume
        return total_volume

    @property
    def components(self):
        all_parts = [self.krokiew, self.murlata, self.jetka, self.lata, self.kontrlata, self.platew, self.slup]
        return [part for part in all_parts if part is not None]
        
    def set_krokiew(self, material: TrussMaterial):
        self.krokiew = material

    def set_murlata(self, material: TrussMaterial):
        self.murlata = material

    def set_jetka(self, material: TrussMaterial):
        self.jetka = material
    
    def set_lata(self, width: float, height: float, laty_spacing: float):
        if self.krokiew is None:
            raise ValueError("Najpierw wprowadź krokiew, aby obliczyć łaty!")
    
        laty_length = math.ceil((self.spacing / 100) * (self.krokiew.quantity - 2))
        quantity = math.ceil(self.krokiew.length / (laty_spacing / 100))

        self.lata = TrussMaterial("Łaty", "lata", None, laty_length, height, width, quantity)
        

    def set_kontrlata(self, width: float, height: float):
        if self.krokiew is None:
            raise ValueError("Najpierw wprowadź krokiew, aby obliczyć kontrłaty!")
        
        kontrlaty_length = self.krokiew.length
        quantity = self.krokiew.quantity

        self.kontrlata = TrussMaterial("Kontrłaty","kontrlata", None, kontrlaty_length, height, width, quantity)

    def set_platew(self, material: TrussMaterial):
        self.platew = material
    
    def set_slup(self, material: TrussMaterial):
        self.slup = material

