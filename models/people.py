from sqlalchemy import Column,Integer,String,Boolean,Float,ForeignKey
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship,Mapped,mapped_column
from config.database import Base
from models.roles import Roles

class People(Base):
    __tablename__= "people"

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String)
    lastname = Column(String)
    carnet = Column(String)
    image = Column(String)
    role_id : Mapped[int] = mapped_column(ForeignKey("public.roles.id"))
    role: Mapped["Roles"] = relationship()
    __table_args__ = {'schema': 'public'}
