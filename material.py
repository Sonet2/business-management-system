import json
import os

import prettytable
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

    for i, wood in enumerate(get_wood_types(data, type_of_wood, subcategory if type_of_wood == "Tarcica" else None)):
        print(f"{i + 1}. {wood}")
    wood_spiece = input("Wybierz gatunek drewna: ")

    how_many_m3 = float(input("Podaj ilość w m3: "))
    length = float(input("Podaj długość w metrach: "))
    if not type_of_wood == "Deska" and not type_of_wood == "Tarcica":
        dimensions = input("Podaj wymiary sztuki (szerokość x wysokość w cm): ")
    else:
        dimensions = input("Podaj grubość sztuki w cm: ")

    wood_price = data[type_of_wood][subcategory][wood_spiece] if subcategory else data[type_of_wood][wood_spiece]

    final_price = how_many_m3 * wood_price


    return{
        "typ": type_of_wood,
        "podkategoria": subcategory,
        "gatunek": wood_spiece,
        "m3": how_many_m3,
        "dlugosc": length,
        "cena_jednostkowa": wood_price,
        "cena_łączna": final_price,
        "wymiary_sztuki": dimensions
    }
def main():
    print("POLMAR")
    print("Obliczanie ceny drewna budowlanego")

    all_orders = []
    czy_zakonczyc = "nie"

    while czy_zakonczyc != "tak":
        all_orders.append(calculate_price())
        czy_zakonczyc = input("Czy chcesz zakończyć operacje zamowienia dla klienta? (tak/nie): ")

        if czy_zakonczyc.lower() == "tak":
            print("Zamowienie dla klienta:")
            table = PrettyTable()
            table.field_names = ["Lp.", "Typ", "Podkategoria", "Gatunek", "Ilość zamówiona (m3)","Długość (m)", "Wymiary sztuki (cm)", "Cena jednostkowa (PLN/m3)", "Cena łączna (PLN)"]
            table.hrules = prettytable.ALL
            for idx, order in enumerate(all_orders, start=1):
                table.add_row([
                    idx,
                    order["typ"],
                    order["podkategoria"] if order["podkategoria"] else "brak",
                    order["gatunek"],
                    order["m3"],
                    order["dlugosc"],
                    order["wymiary_sztuki"],     
                    order["cena_jednostkowa"],
                    order["cena_łączna"],
                ])

            total_m3 = sum(order["m3"] for order in all_orders)
            total_price = sum(order["cena_łączna"] for order in all_orders)

            table.add_row([
                "",
                "SUMA",
                "",
                "",
                total_m3,
                "",
                "",
                "",
                total_price
            ])
            print(table)

            if total_m3 > 9:
                print("UWAGA: Zamówienie przekracza ładowność samochodu! Lepiej zamówić transport zewnetrzny.")


if __name__ == "__main__":
    main()
        