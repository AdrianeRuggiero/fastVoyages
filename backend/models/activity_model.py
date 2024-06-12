from sqlalchemy import Column, Integer, String, ForeignKey
from ..database import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    destination_id = Column(Integer, ForeignKey("destinations.id"))
