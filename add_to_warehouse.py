import json
import os

print("POLMAR")
print("Dodawanie drewna do magazynu")

with open("prices.json", "r") as types_of_wood:
    data = json.load(types_of_wood)

def get_categories(prices): 
    return list(prices.keys())

def get_wood_types(prices, category, subcategory=None):
    if subcategory is None:
        return list(prices[category].keys())
    else:
        return list(prices[category][subcategory].keys())
    
def caltulate_m3(length, width, height):
    return length * width * height

def add_to_warehouse(type_of_wood,subcategory, wood_spiece, m3, length, piece_dimensions):
    try:
        with open("warehouse.json", "r") as warehouse_file:
            warehouse_data = json.load(warehouse_file)
    except (FileNotFoundError, json.JSONDecodeError):
        warehouse_data = []


    new_entry={
        "typ": type_of_wood,
        "podkategoria": subcategory,
        "gatunek": wood_spiece,
        "m3": m3,
        "dlugosc": length,
        "wymiary_sztuki": piece_dimensions,
    }
    warehouse_data.append(new_entry)
    with open("warehouse.json", "w") as warehouse_file:
        json.dump(warehouse_data, warehouse_file, ensure_ascii=False, indent=4)

def adding_material():
    print("Typy drewna:")

    for i, category in enumerate(get_categories(data)):
        print(f"{i + 1}. {category}")
        if category == "Tarcica":
            for j, subcategory in enumerate(get_categories(data[category])):
                print(f"   {j + 1}. {subcategory}")

    type_of_wood = input("Co chcesz dodać?: ")

    if type_of_wood == "Tarcica":
        subcategory = input("Podaj podkategorię: ")
    else:
        subcategory = None

    for i, wood in enumerate(get_wood_types(data, type_of_wood, subcategory if type_of_wood == "Tarcica" else None)):
        print(f"{i + 1}. {wood}")

    wood_spiece = input("Podaj rodzaj drewna: ")
    
    lenght = float(input("Podaj długość (m): "))
    width = float(input("Podaj szerokość (m): "))
    height = float(input("Podaj wysokość (m): "))
    m3 = caltulate_m3(lenght, width, height)
    print(f"Objętość drewna: {m3} m³")
    if type_of_wood == "Tarcica" or type_of_wood =="Deska":
        piece_height = float(input("Podaj grubość sztuki (cm): "))
        piece_dimensions = (f"{piece_height}")
        print(f"Wymiary sztuki: {piece_dimensions} cm")
    else:
        piece_width = float(input("Podaj szerokość sztuki (cm): "))
        piece_height = float(input("Podaj wysokość sztuki (cm): "))
        piece_dimensions = (f"{piece_width}x{piece_height}")
        print(f"Wymiary sztuki: {piece_dimensions} cm")

    add_to_warehouse(type_of_wood, subcategory, wood_spiece, m3, lenght, piece_dimensions)


adding_material()