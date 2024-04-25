from pydantic import BaseModel
from typing import  Optional
from datetime import datetime
from schemas.people_schema import PeopleSchema

class AssistsSchema(BaseModel):
    id:int
    arrivaltime:datetime
    people:PeopleSchema
    class Config:
        orm_mode = True

class AssistsCreateSchema(BaseModel):
    arrivaltime:datetime
    people_id:int
    class Config:
        orm_mode = True