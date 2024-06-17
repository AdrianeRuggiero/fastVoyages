# main.py

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

def extract_flight_information(flight_offer):
    try:
        destination_info = flight_offer.get('destination')
        departure_date = flight_offer.get('departureDate')
        return_date = flight_offer.get('returnDate', None)
        price_total = flight_offer.get('price', {}).get('total', 'N/A')
        links = flight_offer.get('links', {})

        return {
            'destination': destination_info,
            'departure_date': departure_date,
            'return_date': return_date,
            'price_total': price_total,
            'flight_dates_link': links.get('flightDates', 'N/A'),
            'flight_offers_link': links.get('flightOffers', 'N/A')
        }
    except Exception as ex:
        print(f"Erreur lors de l'extraction des informations de vol : {ex}")
        return None

def find_unique_destinations(origin, departure_date, one_way, non_stop, max_price, num_destinations=5):
    try:
        # Obtenir les offres de vols disponibles
        destinations = search_flight_destinations(origin, departure_date, one_way, non_stop, max_price)
        if not destinations or 'data' not in destinations:
            print("Aucune destination trouvée.")
            return []

        flight_offers = destinations['data']

        unique_destinations = []
        seen_destinations = set()

        for offer in flight_offers:
            destination_info = offer.get('destination')
            if destination_info not in seen_destinations and len(unique_destinations) < num_destinations:
                seen_destinations.add(destination_info)
                flight_info = extract_flight_information(offer)
                if flight_info:
                    unique_destinations.append(flight_info)

        return unique_destinations

    except Exception as ex:
        print(f"Erreur : {ex}")
        return []

# Exemple d'utilisation
if __name__ == "__main__":
    origin = 'PAR'  # Code IATA pour Paris
    departure_date = '2024-07-30'  # Date de départ (format YYYY-MM-DD)
    one_way = False  # Vols aller-retour
    non_stop = False  # Vols avec escales
    max_price = 300  # Budget maximum en USD

    num_destinations = 5  # Nombre de destinations uniques à trouver

    unique_destinations = find_unique_destinations(origin, departure_date, one_way, non_stop, max_price, num_destinations)
    if unique_destinations:
        print("Informations sur les 5 destinations uniques :")
        for idx, destination in enumerate(unique_destinations, start=1):
            print(f"{idx}. Destination : {destination['destination']}")
            print(f"   Date de départ : {destination['departure_date']}")
            if destination['return_date']:
                print(f"   Date de retour : {destination['return_date']}")
            print(f"   Prix total : {destination['price_total']}")
            print(f"   Liens vers les détails du vol :")
            print(f"   - Dates de vol : {destination['flight_dates_link']}")
            print(f"   - Offres de vol : {destination['flight_offers_link']}")
            print("\n")
    else:
        print("Aucune destination unique trouvée.")
