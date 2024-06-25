import os
from dotenv import load_dotenv
import requests

# Load environment variables from the .env file
load_dotenv()


def get_access_token():
    """
    Obtain an access token from the Amadeus API using client credentials.

    Returns:
        str: The access token required for API authentication.
    """
    # Retrieve client_id and client_secret from environment variables
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    # URL to obtain the token from the Amadeus API (test mode)
    auth_url = 'https://test.api.amadeus.com/v1/security/oauth2/token'

    # Data for the authentication request
    auth_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    # Make the request to obtain the token
    response = requests.post(auth_url, data=auth_data)
    token_response = response.json()

    # Extract and return the access token
    return token_response.get('access_token')


def create_auth_headers():
    """
    Create authorization headers for the Amadeus API requests.

    Returns:
        dict: A dictionary containing the authorization headers.
    """
    # Obtain the access token
    access_token = get_access_token()

    # Create the authorization headers
    auth_headers = {
        'Authorization': f'Bearer {access_token}'
    }
    return auth_headers
