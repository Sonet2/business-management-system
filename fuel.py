from dotenv import load_dotenv
import requests
import os

load_dotenv()

class Fuel:
    
    def __init__(self, diesel_price_grosze = 650, ors_api_key = None, avg_fuel_per_100 = 14, origin_address = None):
        self.diesel_price_grosze = diesel_price_grosze
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
        try:
            requests_response = requests.get(url, params=params, timeout=10)
            requests_response.raise_for_status()
            data = requests_response.json()
            if not data.get("features"):
                return None
            return data["features"][0]["geometry"]["coordinates"]
        except (requests.exceptions.RequestException, KeyError, IndexError):
            return None
    
    def get_distance(self, origin, destination):
        if origin is None or destination is None:
            return None
        origin = f"{origin[0]},{origin[1]}"
        destination = f"{destination[0]},{destination[1]}"
        url = (f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={self.ors_api_key}&start={origin}&end={destination}")
        
        try:
            requests_response = requests.get(url, timeout=10)
            requests_response.raise_for_status()
            data = requests_response.json() 
            if not data.get("features"):
                return None
            distance = (data["features"][0]["properties"]["summary"]["distance"] / 1000)   
            return (round(distance, 1))

        except (requests.exceptions.RequestException, KeyError, IndexError):
            return None

    def get_route_info(self, destination_address):
        origin_coords = self.geocode_location(self.origin_address)
        destination_coords = self.geocode_location(destination_address)

        if origin_coords is None or destination_coords is None:
            return None

        return self.get_distance(origin_coords, destination_coords)

    def calculate_from_distance(self, distance):
        if distance is None:
            return None
        fuel_consumed  = (distance * self.avg_fuel_per_100) / 100
        fuel_cost = fuel_consumed * self.diesel_price_grosze
        fuel_cost = round(fuel_cost)
        return fuel_cost, fuel_consumed