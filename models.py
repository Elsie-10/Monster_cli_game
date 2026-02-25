from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
from sqlalchemy import Boolean, DateTime


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

class Trade(Base):
    __tablename__ = 'trades'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('players.id'))
    receiver_id = Column(Integer, ForeignKey('players.id'))
    monster_id = Column(Integer, ForeignKey('player_monsters.id'))
    status = Column(String) # e.g., 'Pending', 'Completed'

class PlayerAchievement(Base):
    __tablename__ = 'player_achievements'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    achievement_id = Column(Integer, ForeignKey('achievements.id'))
    achieved_at = Column(DateTime, default=datetime.utcnow)
    is_claimed = Column(Boolean, default=False)

    player = relationship("Player", back_populates="achievements")

class Battle(Base):
    __tablename__ = 'battles'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    opponent_id = Column(Integer) # Can be another player_id or a NPC_id
    winner_id = Column(Integer)
    battle_date = Column(DateTime, default=datetime.utcnow)
    xp_gained = Column(Integer)

class Achievement(Base):
    __tablename__ = 'achievements'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    requirement_val = Column(Integer)