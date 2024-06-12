from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import flight_model
from ..schemas import flight_schema

# Crée un routeur pour les vols
router = APIRouter()

# Endpoint pour obtenir les vols par ID de destination
@router.get("/flights/{destination_id}", response_model=List[flight_schema.Flight])
def get_flights(destination_id: int, db: Session = Depends(get_db)):
    # Recherche les vols dans la base de données pour la destination donnée
    flights = db.query(flight_model.Flight).filter(flight_model.Flight.destination_id == destination_id).all()
    # Si aucun vol n'est trouvé, renvoie une erreur 404
    if not flights:
        raise HTTPException(status_code=404, detail="No flights found for this destination")
    return flights

# Endpoint pour créer un nouveau vol
@router.post("/flights", response_model=flight_schema.Flight)
def create_flight(flight: flight_schema.FlightCreate, db: Session = Depends(get_db)):
    # Crée un nouvel objet vol à partir des données fournies
    db_flight = flight_model.Flight(**flight.dict())
    # Ajoute et enregistre le nouveau vol dans la base de données
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight
