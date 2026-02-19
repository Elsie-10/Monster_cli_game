from sqlalchemy import Column, Integer, String, Float,DateTime, Boolean
from database import Base
from datetime import datetime 

class MonsterSpecies(Base):
    __tablename__= 'monster_species'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    element_type = Column(String) # Fire, Water
    base_hp = Column(Integer)
    base_attack = Column(Integer)
    base_defense = Column(Integer)
    rarity = Column(Integer) # 1(common) to 10(Legendary)

    instances = relationship("PlayerMonster", back_populates="species")
