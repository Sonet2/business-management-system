import json
import os

def main():
    print("POLMAR")
    print("Dodawanie drewna do magazynu")

    print("Wybierz opcję:")
    print("1. Dodaj drewno do magazynu")
    print("2. Sprawdź stan magazynu")
    print("3. Usuń drewno z magazynu")
    option = input("Wprowadź numer opcji: ")
    czy_zakonczyc = "nie"   
    while czy_zakonczyc != "tak":
        if option == "1":
            adding_material()
        elif option == "2":
            warehouse_status()
        elif option == "3":
            delete_material()
        else:
            print("Nieprawidłowa opcja. Proszę wybrać 1, 2 lub 3.")
        czy_zakonczyc = input("Czy chcesz zakończyć operacje w magazynie? (tak/nie): ")

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

def write_to_warehouse(type_of_wood,subcategory, wood_spiece, m3, length, piece_dimensions):
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

    try:
        write_to_warehouse(type_of_wood, subcategory, wood_spiece, m3, lenght, piece_dimensions)
    except Exception as e:
        print(f"Wystąpił błąd podczas zapisywania danych: {e}")

def warehouse_status():
    try:
        with open("warehouse.json", "r") as warehouse:
            data = json.load(warehouse)
    except FileNotFoundError:
        print("Brak danych w magazynie.")
        return[]
    except json.JSONDecodeError:
        print("Błąd odczytu danych magazynu.")
        return[]   
    
    print("Stan magazynu:")
    print("")
    for i, entry in enumerate(data):
        podkategoria = f"{entry['podkategoria']}" if entry['podkategoria'] is not None else ""
        print(f"{i + 1}. {entry['typ']} {podkategoria} - ({entry['gatunek']}) - {entry['m3']} m³, długość: {entry['dlugosc']} m, wymiary sztuki: {entry['wymiary_sztuki']} cm")
        print("")

def delete_material():
    try:
        with open("warehouse.json", "r") as warehouse:
            data = json.load(warehouse)
    except FileNotFoundError:
        print("Brak danych w magazynie.")
        return[]
    except json.JSONDecodeError:
        print("Błąd odczytu danych magazynu.")
        return[]   
    
    print("Stan magazynu:")
    print("")
    for i, entry in enumerate(data):
        podkategoria = f"{entry['podkategoria']}" if entry['podkategoria'] is not None else ""
        print(f"{i + 1}. {entry['typ']} {podkategoria} - ({entry['gatunek']}) - {entry['m3']} m³, długość: {entry['dlugosc']} m, wymiary sztuki: {entry['wymiary_sztuki']} cm")
        print("")    
    
    delete =int(input("Podaj numer pozycji do usunięcia: "))
    if 1 <= delete <= len(data):
        del data[delete - 1]
        print("Pozycja została usunięta.")
        with open("warehouse.json", "w") as warehouse:
            json.dump(data, warehouse, ensure_ascii=False, indent=4)    

if __name__ == "__main__":
    main()


