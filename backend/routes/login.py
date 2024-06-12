from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import user_model
from ..schemas import user_schema
from ..services.auth_service import authenticate_user, create_access_token

# Crée un routeur pour l'authentification
router = APIRouter()

# Endpoint pour se connecter et obtenir un token d'accès
@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(form_data: user_schema.Login, db: Session = Depends(get_db)):
    # Authentifie l'utilisateur en vérifiant le nom d'utilisateur et le mot de passe
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        # Si l'authentification échoue, renvoie une erreur 400
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )
    # Crée un token d'accès JWT pour l'utilisateur authentifié
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
