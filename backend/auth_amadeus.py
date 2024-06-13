import os
from dotenv import load_dotenv
import requests

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

def get_access_token():
    # Récupérer les valeurs de client_id et client_secret depuis les variables d'environnement
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    # URL pour obtenir le token de l'API Amadeus (mode test)
    auth_url = 'https://test.api.amadeus.com/v1/security/oauth2/token'

    # Données pour la requête d'authentification
    auth_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    # Faire la requête pour obtenir le token
    response = requests.post(auth_url, data=auth_data)
    token_response = response.json()

    # Extraire et retourner le token d'accès
    return token_response.get('access_token')

def create_auth_headers():
    access_token = get_access_token()
    auth_headers = {
        'Authorization': f'Bearer {access_token}'
    }
    return auth_headers
