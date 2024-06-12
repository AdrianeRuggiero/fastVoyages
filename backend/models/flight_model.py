from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    destination_id = Column(Integer, ForeignKey("destinations.id"))

    # Si nécessaire, définissez une relation avec la table de destination
    destination = relationship("Destination", back_populates="flights")
