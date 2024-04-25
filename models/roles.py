from sqlalchemy import Column,Integer,String
from config.database import Base

class Roles(Base):
    __tablename__= "roles"

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String)
    description = Column(String)
    __table_args__ = {'schema': 'public'}
