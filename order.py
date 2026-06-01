import fuel_road, material, truss
import json
import os
from dotenv import load_dotenv

load_dotenv()
origin = os.getenv("START_ADDRESS")

def main():
    print("POLMAR")
    print("Kompletowanie zamówienia dla klienta")
    print("Wybierz opcję:")
    print("1. Deski / Materiał luźny")
    print ("2. Więźba dachowa")
    option = input("Twoj wybor: ")
    
    if option == "1":

        name = input("Imie klienta: ")
        if not name.isalpha():
            print("Nieprawidłowe imię")
            return None
        surname = input("Nazwisko klienta: ")
        if not surname.isalpha():
            print("Nieprawidłowe nazwisko")
            return None

        destination = input("Podaj adres klienta: ")
        
        origin_coords = fuel_road.geocode_location(origin)
        destination_coords = fuel_road.geocode_location(destination)

        if origin_coords is None or destination_coords is None:
            print("Nie można znaleźć lokalizacji. Sprawdź wprowadzone adresy i spróbuj ponownie.")
            return None
        else:
            route_info = fuel_road.calculate_fuel_cost(origin_coords, destination_coords, destination)

        full_order_info = material.main()
        

        order_summary = {
            "imie": name,
            "nazwisko": surname,
            "dojazd" : route_info,
            "zamowienie": full_order_info
        }
        
        try:
            with open("orders.json", "r+", encoding="utf-8") as order_file:
                try:
                    file_data = json.load(order_file)
                except json.JSONDecodeError:
                    file_data = []
                if isinstance(file_data, dict):
                    file_data = [file_data]
                file_data.append(order_summary)
                order_file.seek(0)
                json.dump(file_data, order_file, ensure_ascii=False, indent=4)
                order_file.truncate()
        except FileNotFoundError:
            with open("orders.json", "w", encoding="utf-8") as order_file:
                json.dump([order_summary], order_file, ensure_ascii=False, indent=4)
        

    elif option == "2":
        name = input("Imie klienta: ")
        if not name.isalpha():
            print("Nieprawidłowe imię.")
            return None
        surname = input("Nazwisko klienta: ")
        if not surname.isalpha():
            print("Nieprawidłowe nazwisko.")
            return None

        destination = input("Podaj adres klienta: ")
        
        origin_coords = fuel_road.geocode_location(origin)
        destination_coords = fuel_road.geocode_location(destination)

        if origin_coords is None or destination_coords is None:
            print("Nie można znaleźć lokalizacji. Sprawdź wprowadzone adresy i spróbuj ponownie.")
            return None
        else:
            route_info = fuel_road.calculate_fuel_cost(origin_coords, destination_coords, destination)

        full_order_info = truss.main()
        

        order_summary = {
            "imie": name,
            "nazwisko": surname,
            "dojazd" : route_info,
            "zamowienie": full_order_info
        }
        
        try:
            with open("orders.json", "r+", encoding="utf-8") as order_file:
                try:
                    file_data = json.load(order_file)
                except json.JSONDecodeError:
                    file_data = []
                if isinstance(file_data, dict):
                    file_data = [file_data]
                file_data.append(order_summary)
                order_file.seek(0)
                json.dump(file_data, order_file, ensure_ascii=False, indent=4)
                order_file.truncate()

        except FileNotFoundError:
            with open("orders.json", "w", encoding="utf-8") as order_file:
                json.dump([order_summary], order_file, ensure_ascii=False, indent=4)

        except json.JSONDecodeError:
            with open("orders.json", "w", encoding="utf-8") as order_file:
                json.dump([order_summary], order_file, ensure_ascii=False, indent=4)
        
             

if __name__ == "__main__":
    main()