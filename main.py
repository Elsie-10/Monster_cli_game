from Database.database import engine
from sqlalchemy.orm import declarative_base
from Database.player import Player
from .Monster_species import MonsterSpecies
from .Player_achievements import PlayerAchievement
from .Player_Monster import PlayerMonster
from .Trade import Trade 
from .Battle import Battle 
from .Achievement import Achievement

Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!")
