from sqlalchemy import Column, Integer, String, Float,DateTime, Boolean
from .database import Base
from datetime import datetime 

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    level = Column(Integer, default=1)
    experience = Column(Integer, deault=0)
    currency = Column(Integer, default=100)

    #relationship
    monsters = relationship("PlayerMonster", back_populates="owner")
    achievements = relationship("PlayerAchievement", back_populates="player")
