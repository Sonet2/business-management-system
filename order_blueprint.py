class OrderBlueprint:
    def __init__(self, name, surname, route_info, material_data):
        self.name = name
        self.surname = surname
        self.route_info = route_info
        self.material_data = material_data

    def to_dict(self):
        return {
            "imie": self.name,
            "nazwisko": self.surname,
            "informacje_o_drodze": self.route_info,
            "dane_materialu": self.material_data.to_dict() if self.material_data else None
        }

    @classmethod
    def from_dict(cls, data):
        name = data.get("imie")
        surname = data.get("nazwisko")
        route_info = data.get("informacje_o_drodze")
        material_data_dict = data.get("dane_materialu")
        material_data = cls.material_class.from_dict(material_data_dict) if material_data_dict else None
        return cls(name, surname, route_info, material_data)
