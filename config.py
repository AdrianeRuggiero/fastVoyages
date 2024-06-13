import os
from dotenv import load_dotenv

# Charger les variables d'environnement à partir de .env
load_dotenv()

AMADEUS_API_KEY = os.getenv('AMADEUS_API_KEY')
AMADEUS_API_SECRET = os.getenv('AMADEUS_API_SECRET')
