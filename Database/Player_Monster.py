from sqlalchemy import Column, Integer, String, Float,DateTime, Boolean
from database import Base
from datetime import datetime 

class PlayerMonster(Base):
    __tablename__ = 'player_monsters'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    species_id = Column(Integer, ForeignKey('monster_species.id'))
    
    nickname = Column(String)
    level = Column(Integer, default=1)
    current_hp = Column(Integer)
    experience = Column(Integer, default=0)
    
    # Relationships
    owner = relationship("Player", back_populates="monsters")
    species = relationship("MonsterSpecies", back_populates="instances")