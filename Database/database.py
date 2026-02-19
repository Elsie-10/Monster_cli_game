from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .player import Player
from .Monster_species import MonsterSpecies
from .Player_achievements import PlayerAchievement
from .Player_Monster import PlayerMonster
from .Trade import Trade 
from .Battle import Battle 
from .Achievement import Achievement

DATABASE_URL = "sqlite:///monster_game.db"

engine = create_engine(DATABASE_URL, echo=True)

sessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()

# What this does;
# Creates SQLite database file monster_game.db
#sets up session factory
#Create Base class for models