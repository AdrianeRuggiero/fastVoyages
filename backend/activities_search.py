import requests
from auth_amadeus import create_auth_headers
from geocoding import get_coordinates

def search_activities(latitude=None, longitude=None, radius=1, city_name=None):
    try:
        if city_name:
            latitude, longitude = get_coordinates(city_name)
        elif latitude is None or longitude is None:
            raise ValueError("Either city_name or both latitude and longitude must be provided")

        url = 'https://test.api.amadeus.com/v1/shopping/activities'
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'radius': radius
        }
        
        headers = create_auth_headers()
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"Erreur HTTP : {http_err}")
        print(f"Réponse de l'API : {response.content}")
        return None
    except Exception as err:
        print(f"Erreur : {err}")
        return None


def display_top_activities(city_name, radius):
    # Rechercher les activités dans la ville spécifiée avec un rayon donné
    activities_response = search_activities(city_name=city_name, radius=radius)

    if activities_response:
        # Extraire la liste d'activités du dictionnaire de réponse
        activities = activities_response.get('data', [])

        # Afficher seulement les 4 premières activités si elles existent
        top_activities = activities[:4]
        for index, activity in enumerate(top_activities, start=1):
            print(f"Activité {index}: {activity['name']}")
            print(f"    Description: {activity.get('shortDescription', 'Pas de description disponible')}")
            print(f"    Prix: {activity.get('price', 'Information de prix non disponible')}")
            print(f"    Durée: {activity.get('duration', 'Information de durée non disponible')}")
            print(f"    Lieu: {activity.get('location', {}).get('address', 'Adresse non disponible')}")
            print("")

    else:
        print("La recherche d'activités a échoué.")

# Exemple d'utilisation
if __name__ == "__main__":
    city_name = "Barcelone"
    radius = 1  # en kilomètres

    display_top_activities(city_name, radius)