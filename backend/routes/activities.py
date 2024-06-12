from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import activity_model
from ..schemas import activity_schema

# Crée un routeur pour les activités
router = APIRouter()

# Endpoint pour obtenir les activités par ID de destination
@router.get("/activities/{destination_id}", response_model=List[activity_schema.Activity])
def get_activities(destination_id: int, db: Session = Depends(get_db)):
    # Recherche les activités dans la base de données pour la destination donnée
    activities = db.query(activity_model.Activity).filter(activity_model.Activity.destination_id == destination_id).all()
    # Si aucune activité n'est trouvée, renvoie une erreur 404
    if not activities:
        raise HTTPException(status_code=404, detail="No activities found for this destination")
    return activities

# Endpoint pour créer une nouvelle activité
@router.post("/activities", response_model=activity_schema.Activity)
def create_activity(activity: activity_schema.ActivityCreate, db: Session = Depends(get_db)):
    # Crée un nouvel objet activité à partir des données fournies
    db_activity = activity_model.Activity(**activity.dict())
    # Ajoute et enregistre la nouvelle activité dans la base de données
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity
