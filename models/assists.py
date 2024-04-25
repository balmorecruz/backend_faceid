from sqlalchemy import Column,Integer,String,Boolean,Float,ForeignKey
from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.sql import func
from config.database import Base
from sqlalchemy.orm import relationship,Mapped,mapped_column
from models.people import People
import datetime

class Assists(Base):
    __tablename__= "assists"

    id = Column(Integer,primary_key=True,autoincrement=True)
    arrivaltime: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())
    people_id : Mapped[int] = mapped_column(ForeignKey("public.people.id"))
    people: Mapped["People"] = relationship()
    __table_args__ = {'schema': 'public'}
