from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./recipes.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class RecipeHistory(Base):
    __tablename__ = "recipe_history"

    id = Column(Integer, primary_key=True, index=True)
    recipe_name = Column(String)
    ingredients = Column(String)

Base.metadata.create_all(bind=engine)