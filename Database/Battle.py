from sqlalchemy import Column, Integer, String, Float,DateTime, Boolean
from database import Base
from datetime import datetime 

class Battle(Base):
    __tablename__ = 'battles'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    opponent_id = Column(Integer) # Can be another player_id or a NPC_id
    winner_id = Column(Integer)
    battle_date = Column(DateTime, default=datetime.utcnow)
    xp_gained = Column(Integer)