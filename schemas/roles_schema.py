from pydantic import BaseModel
from typing import  Optional

class RolesSchema(BaseModel):
    id:int
    name:str
    description:str
    class Config:
        orm_mode = True