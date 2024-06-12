from fastapi import APIRouter

# Crée un routeur pour la page d'accueil
router = APIRouter()

# Endpoint pour la racine de l'API
@router.get("/")
def read_root():
    # Renvoie un message de bienvenue
    return {"message": "Welcome to FastVoyage API!"}
