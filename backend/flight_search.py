import requests
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

def get_access_token():
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    auth_url = 'https://test.api.amadeus.com/v1/security/oauth2/token'

    auth_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(auth_url, data=auth_data)
    try:
        response.raise_for_status()  # Lever une erreur si la requête échoue
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        print(f"Response: {response.text}")
        raise

    token_response = response.json()

    access_token = token_response.get('access_token')
    if access_token:
        print("Access token obtained successfully:", access_token)
    else:
        print("Failed to obtain access token. Response:", token_response)

    return access_token

def create_auth_headers():
    access_token = get_access_token()
    if not access_token:
        raise ValueError("Access token is None. Cannot create auth headers.")
    print("Authorization Header:", f'Bearer {access_token}')
    return {
        'Authorization': f'Bearer {access_token}'
    }

def search_flights(origin, budget, departure_date, return_date):
    url = 'https://test.api.amadeus.com/v1/shopping/flight-offers'
    params = {
        'origin': origin,
        'maxPrice': budget,
        'departureDate': departure_date,
        'returnDate': return_date
    }
    headers = create_auth_headers()
    print(f"Request URL: {url}")
    print(f"Request Headers: {headers}")
    print(f"Request Params: {params}")
    response = requests.get(url, headers=headers, params=params)
    try:
        response.raise_for_status()  # Lever une erreur si la requête échoue
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        print(f"Response: {response.text}")
        raise
    return response.json()

# Exemple d'utilisation
if __name__ == "__main__":
    origin = "CDG"  # Paris Charles de Gaulle
    budget = 500
    departure_date = "2023-07-01"
    return_date = "2023-07-15"
    try:
        flights = search_flights(origin, budget, departure_date, return_date)
        print(flights)
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")
