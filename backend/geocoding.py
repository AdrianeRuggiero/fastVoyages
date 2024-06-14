import os
from dotenv import load_dotenv
from opencage.geocoder import OpenCageGeocode

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

def get_coordinates(city_name):
    api_key = os.getenv('OPENCAGE_API_KEY')
    geocoder = OpenCageGeocode(api_key)
    results = geocoder.geocode(city_name)

    if results and len(results) > 0:
        latitude = results[0]['geometry']['lat']
        longitude = results[0]['geometry']['lng']
        return latitude, longitude
    else:
        raise ValueError(f"Unable to find coordinates for city: {city_name}")

# Exemple d'utilisation
if __name__ == "__main__":
    city_name = "Paris"
    try:
        lat, lng = get_coordinates(city_name)
        print(f"Coordinates of {city_name}: Latitude={lat}, Longitude={lng}")
    except ValueError as e:
        print(e)
