# Fuel prices are currently hardcoded because there is no free fuel price API available online.
# This logic lives in a separate file so it can be expanded later, once web scraping is learned.
import requests
from dotenv import load_dotenv
import os

load_dotenv()
ors_api_key = os.getenv("ORS_API_KEY")
diesel_price = 6.50
 
def geocode_location(address):
    url = "https://api.openrouteservice.org/geocode/search"
    params={
        "api_key": ors_api_key,
        "text": address,
        "boundary.country": "PL",
        "size": 1
    }
    requests_response = requests.get(url, params=params)
    try:
        requests_response.raise_for_status()
        data = requests_response.json()
        return data["features"][0]["geometry"]["coordinates"]
    except (requests.exceptions.HTTPError, IndexError):
        print("Nie można znaleźć lokalizacji. Sprawdź wprowadzony adres i spróbuj ponownie.")
        return None
    
def get_distance(origin, destination):
    origin = f"{origin[0]},{origin[1]}"
    destination = f"{destination[0]},{destination[1]}"
    url = (f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={ors_api_key}&start={origin}&end={destination}")
    requests_response = requests.get(url)
    try:
        requests_response.raise_for_status()
        data = requests_response.json() 
        distance = (data["features"][0]["properties"]["summary"]["distance"] / 1000)   
        return (round(distance, 1))

    except (requests.exceptions.HTTPError, KeyError):
        print("Nie można obliczyć trasy. Sprawdź wprowadzone adresy i spróbuj ponownie.")
        return None


def calculate_fuel_cost(origin, destination):
    distance = get_distance(origin, destination)
    avg_fuel_per_100 = 14
    if distance is not None:
        fuel_cost = (distance / 100) * avg_fuel_per_100 * diesel_price
        fuel_consumed = (distance / 100) * avg_fuel_per_100
        
        print(f"Dystans wynosi: {distance} km")
        print(f"Szacowany koszt paliwa na trasie wynosi: {round(fuel_cost, 2)} zł")
        print(f"Szacowana ilość paliwa, która zostanie zużyta na trasie: {round(fuel_consumed, 2)} litrów")

def main():
    print("POLMAR")
    print("Obliczanie kosztów paliwa na trasie")
    origin = geocode_location(input("Podaj miejsce startu: "))
    destination = geocode_location(input("Podaj miejsce docelowe: "))

    calculate_fuel_cost(origin, destination)


if __name__ == "__main__":
    main()
