from pydantic import BaseModel

class FlightBase(BaseModel):
    name: str
    description: str

class FlightCreate(FlightBase):
    destination_id: int

class Flight(FlightBase):
    id: int

    class Config:
        orm_mode = True
