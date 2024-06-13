import requests

#Vos valeurs de client_id et client_secret
client_id = '2oLgGem4uR8wI2cgRG1egdkWIbsUIKHf'
client_secret = 'wXJaWYA2iWxL8Xxj'

#URL pour obtenir le token d'authentification
auth_url = 'https://test.api.amadeus.com/v1/security/oauth2/token'  # Utilisez 'https://api.amadeus.com/v1/security/oauth2/token' pour la production

#Données pour la requête d'authentification
auth_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret
}

#En-têtes pour la requête d'authentification
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

#Faire la requête pour obtenir le token
response = requests.post(auth_url, data=auth_data, headers=headers)
token_response = response.json()

#Extraire le token de la réponse
access_token = token_response['access_token']

#Configurer l'en-tête d'authentification pour les requêtes suivantes
auth_headers = {
    'Authorization': f'Bearer {access_token}'
}

# #Exemple de requête pour obtenir les destinations de la compagnie aérienne British Airways (BA)
# url = 'https://test.api.amadeus.com/v1/airline/destinations'  # Utilisez 'https://api.amadeus.com/v1/airline/destinations' pour la production
# params = {
#     'airlineCode': 'BA'
# }

# #Faire la requête en utilisant le token d'authentification
# response = requests.get(url, headers=auth_headers, params=params)

#Imprimer les données de la réponse
print(response.json())