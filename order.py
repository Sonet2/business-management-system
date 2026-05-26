import fuel_road, material
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
        surname = input("Nazwisko klienta: ")


        destination = input("Podaj adres klienta: ")
        
        origin_coords = fuel_road.geocode_location(origin)
        destination_coords = fuel_road.geocode_location(destination)

        if origin_coords is None or destination_coords is None:
            print("Nie można znaleźć lokalizacji. Sprawdź wprowadzone adresy i spróbuj ponownie.")
            return None
        else:
            route_info = fuel_road.calculate_fuel_cost(origin_coords, destination_coords)

        full_order_info = material.main()
        

        order_summary = {
            "imie": name,
            "nazwisko": surname,
            "dojazd" : route_info,
            "zamowienie": full_order_info
        }

        with open("orders.json", "w") as order_file:
            json.dump(order_summary, order_file, ensure_ascii=False, indent=4)
            print("Pomyślnie dodano zamowienie do bazy danych.")

    elif option == "2":
        print("Opcja w trakcie realizacji. Prosimy o cierpliwość.")
        pass
        
             

if __name__ == "__main__":
    main()