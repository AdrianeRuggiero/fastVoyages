from fastapi import FastAPI
from .routes import activities, flights, home, login, register
from .database import engine, Base

# Crée toutes les tables de la base de données
Base.metadata.create_all(bind=engine)

# Crée l'application FastAPI
app = FastAPI()

# Inclut les routeurs dans l'application FastAPI
app.include_router(activities.router, prefix="/api")
app.include_router(flights.router, prefix="/api")
app.include_router(home.router, prefix="/api")
app.include_router(login.router, prefix="/api")
