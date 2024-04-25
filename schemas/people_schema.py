from pydantic import BaseModel
from typing import  Optional
from datetime import datetime
from schemas.roles_schema import RolesSchema

class PeopleSchema(BaseModel):
    id:int
    name:str
    lastname:str
    carnet:str
    image:str
    role:RolesSchema
    class Config:
        orm_mode = True

class PeopleCreateSchema(BaseModel):
    name:str
    lastname:str
    carnet:str
    image:str
    role_id:int
    class Config:
        orm_mode = True