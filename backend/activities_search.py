import requests
from auth_amadeus import create_auth_headers


def search_activities(latitude, longitude, radius):
    try:
        # Construire l'URL avec les paramètres spécifiés
        url = f'https://test.api.amadeus.com/v1/shopping/activities'
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'radius': radius
        }
        
        headers = create_auth_headers()

        # Faire la requête GET avec les headers d'authentification et les paramètres
        response = requests.get(url, headers=headers, params=params)

        # Vérifier le statut de la réponse
        response.raise_for_status()

        # Retourner les données JSON de la réponse
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"Erreur HTTP : {http_err}")
    except Exception as err:
        print(f"Erreur : {err}")

# Exemple d'utilisation
if __name__ == "__main__":
    latitude = 41.397158
    longitude = 2.160873
    radius = 1  # en kilomètres

    activities = search_activities(latitude, longitude, radius)
    if activities:
        print(activities)
    else:
        print("La recherche d'activités a échoué.")