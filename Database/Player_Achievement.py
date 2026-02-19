from sqlalchemy import Column, Integer, String, Float,DateTime, Boolean
from database import Base
from datetime import datetime 


class PlayerAchievement(Base):
    __tablename__ = 'player_achievements'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    achievement_id = Column(Integer, ForeignKey('achievements.id'))
    achieved_at = Column(DateTime, default=datetime.utcnow)
    is_claimed = Column(Boolean, default=False)

    player = relationship("Player", back_populates="achievements")