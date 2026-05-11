import json

print("POLMAR")
print("Dodawanie drewna do magazynu")

with open("prices.json", "r") as typy_drewna:
    data = json.load(typy_drewna)

def get_categories(prices):
    return list(prices.keys())
def get_wood_types(prices, category, subcategory=None):
    if subcategory is None:
        return list(prices[category].keys())
    else:
        return list(prices[category][subcategory].keys())

def adding_material():
    print("Typy drewna:")

    for i, category in enumerate(get_categories(data)):
        print(f"{i + 1}. {category}")
        if category == "Tarcica":
            for j, subcategory in enumerate(get_categories(data[category])):
                print(f"   {j + 1}. {subcategory}")

    name = input("Co chcesz dodać?: ")
    if name == "Tarcica":
        subcategory = input("Podaj podkategorię: ")
    for i, wood in enumerate(get_wood_types(data, name, subcategory if name == "Tarcica" else None)):
        print(f"{i + 1}. {wood}")
    type_of_wood = input("Podaj rodzaj drewna: ")
    if(input("Czy jest to paczka czy pojedyncze sztuki? (paczka/pojedyncze): ") == "paczka"):
            print("Podaj wymiary paczki:")
            lenght = float(input("Podaj długość: "))
            width = float(input("Podaj szerokość: "))
            height = float(input("Podaj wysokość: "))
            volume = lenght * width * height
    else:
        quantity = int(input("Podaj liczbę sztuk: "))
        lenght = float(input("Podaj długość sztuki: "))
        width = float(input("Podaj szerokość sztuki: "))
        height = float(input("Podaj wysokość sztuki: "))
        volume = lenght * width * height * quantity

adding_material()