import requests, math
from dotenv import load_dotenv
import os

load_dotenv()

class Fuel:
    
    def __init__(self, diesel_price = 6.50, ors_api_key = None, avg_fuel_per_100 = 14, origin_address = None):
        self.diesel_price = diesel_price
        self.ors_api_key = ors_api_key or os.getenv("ORS_API_KEY")
        self.avg_fuel_per_100 = avg_fuel_per_100
        self.origin_address = origin_address or os.getenv("START_ADDRESS")

    def geocode_location(self, address):
        if address is None or address.strip() == "":
            return None
        url = "https://api.openrouteservice.org/geocode/search"
        params={
            "api_key": self.ors_api_key,
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
            return None
    
    def get_distance(self, origin, destination):
        if origin is None or destination is None:
            return None
        origin = f"{origin[0]},{origin[1]}"
        destination = f"{destination[0]},{destination[1]}"
        url = (f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={self.ors_api_key}&start={origin}&end={destination}")
        requests_response = requests.get(url)
        try:
            requests_response.raise_for_status()
            data = requests_response.json() 
            distance = (data["features"][0]["properties"]["summary"]["distance"] / 1000)   
            return (round(distance, 1))

        except (requests.exceptions.HTTPError, KeyError):
            return None
        
    def calculate_fuel_cost(self, origin, destination, destination_name):
        distance = self.get_distance(origin, destination)
        dest = destination_name
        if distance is None:
            return None
        else:
            fuel_cost = (distance / 100) * self.avg_fuel_per_100 * self.diesel_price
            fuel_consumed = (distance / 100) * self.avg_fuel_per_100
            
            fuel_info = {
                "adres_dostawy": dest,
                "dystans": distance,
                "koszt_paliwa": math.ceil(fuel_cost),
                "zużycie_paliwa": math.ceil(fuel_consumed)
            }
            return fuel_info
    def get_route_info(self, destination_address):
        origin_coords = self.geocode_location(self.origin_address)
        destination_coords = self.geocode_location(destination_address)
        if origin_coords is None or destination_coords is None:
            return None
        route_info = self.calculate_fuel_cost(origin_coords, destination_coords, destination_address)
        return route_info