import json

from prettytable import PrettyTable

with open("prices.json", "r") as types_of_wood:
    data = json.load(types_of_wood)

def get_categories(prices): 
    return list(prices.keys())

def get_wood_types(prices, category, subcategory=None):
    if subcategory is None:
        return list(prices[category].keys())
    else:
        return list(prices[category][subcategory].keys())
    
def calculate_price():

    for i, category in enumerate(get_categories(data)):
        print(f"{i + 1}. {category}")
        if category == "Tarcica":
            for j, subcategory in enumerate(get_categories(data[category])):
                print(f"   {j + 1}. {subcategory}")
    
    type_of_wood = input("Wybierz typ drewna: ")
    if type_of_wood == "Tarcica":
        subcategory = input("Podaj podkategorię: ")
    else:
        subcategory = None

    # Pobierz wpis z cennika dla wybranego typu
    entry = data[type_of_wood]
    if not isinstance(entry, dict):
        # entry to bezpośrednia cena (np. Łaty, Kontrłaty)
        wood_spiece = None
        wood_price = entry
    else:
        # entry to słownik gatunków lub podkategoria (Tarcica)
        if type_of_wood == "Tarcica" and subcategory:
            options = list(entry[subcategory].keys())
        else:
            options = list(entry.keys())
        for i, wood in enumerate(options):
            print(f"{i + 1}. {wood}")
        wood_spiece = input("Wybierz gatunek drewna: ")
        if type_of_wood == "Tarcica" and subcategory:
            wood_price = entry[subcategory].get(wood_spiece, 0)
        else:
            wood_price = entry.get(wood_spiece, 0)

    how_many_m3 = float(input("Podaj ilość w m3: "))
    length = float(input("Podaj długość w metrach: "))
    if not type_of_wood == "Deska" and not type_of_wood == "Tarcica":
        dimensions = input("Podaj wymiary sztuki (szerokość x wysokość w cm): ")
    else:
        dimensions = input("Podaj grubość sztuki w cm: ")

    final_price = how_many_m3 * wood_price


    return{
        "typ": type_of_wood,
        "podkategoria": subcategory,
        "gatunek": wood_spiece,
        "m3": how_many_m3,
        "dlugosc": length,
        "cena_jednostkowa": wood_price,
        "cena_laczna": final_price,
        "wymiary_sztuki": dimensions
    }
def main():
    print("Kompletowanie materiałów dla klienta")

    all_orders = []
    czy_zakonczyc = "nie"

    while czy_zakonczyc != "tak":
        all_orders.append(calculate_price())
        czy_zakonczyc = input("Czy chcesz zakończyć dodawanie materiałów? (tak/nie): ")

        if czy_zakonczyc.lower() == "tak":
            total_cost = sum(order["cena_laczna"] for order in all_orders)
            total_m3 = sum(order["m3"] for order in all_orders)

            
            full_order_info = {
                "laczny_metraz": total_m3,
                "laczna_cena": total_cost,
                "pozycje": all_orders
                
            }
            return full_order_info




if __name__ == "__main__":
    main()
        