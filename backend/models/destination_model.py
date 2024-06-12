from sqlalchemy import Column, Integer, String
from ..database import Base

class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
