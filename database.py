from sqlalchemy import create_all
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "sqlite:///monster_game.db"

engine = create_engine(DATABASE_URL, echo=True)

sessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()
def init_db():
    Base.metadata.create_all(engine)

# What this does;
# Creates SQLite database file monster_game.db
#sets up session factory
#Create Base class for models