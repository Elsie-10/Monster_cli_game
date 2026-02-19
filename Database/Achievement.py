from sqlalchemy import Column, Integer, String, Float,DateTime, Boolean
from database import Base
from datetime import datetime 

class Achievement(Base):
    __tablename__ = 'achievements'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    requirement_val = Column(Integer)