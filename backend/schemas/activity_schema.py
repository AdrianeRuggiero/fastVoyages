from pydantic import BaseModel

class ActivityBase(BaseModel):
    name: str
    description: str

class ActivityCreate(ActivityBase):
    destination_id: int

class Activity(ActivityBase):
    id: int

    class Config:
        orm_mode = True
