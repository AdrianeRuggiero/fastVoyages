import requests
from auth_amadeus import create_auth_headers

def search_flight_destinations(origin, departure_date, one_way, non_stop, max_price):
    try:
        url = 'https://test.api.amadeus.com/v1/shopping/flight-destinations'
        params = {
            'origin': origin,
            'departureDate': departure_date,
            'oneWay': one_way,
            'nonStop': non_stop,
            'maxPrice': max_price
        }

        headers = create_auth_headers()

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"Erreur HTTP : {http_err}")
        print(f"Réponse de l'API : {response.content}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"Erreur de requête : {req_err}")
        return None
    except Exception as ex:
        print(f"Erreur inattendue : {ex}")
        return None

# Exemple d'utilisation
if __name__ == "__main__":
    origin = 'PAR'  # Code IATA pour Madrid
    departure_date = '2024-07-30'  # Date de départ (format YYYY-MM-DD)
    one_way = False  # Vols aller-retour
    non_stop = False  # Vols avec escales
    max_price = 300  # Budget maximum en USD

    destinations = search_flight_destinations(origin, departure_date, one_way, non_stop, max_price)
    if destinations:
        print(destinations)
    else:
        print("La recherche de destinations de vol a échoué.")