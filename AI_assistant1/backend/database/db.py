from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String
)

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker
)

DATABASE_URL = "sqlite:///./recipes.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class RecipeHistory(Base):

    __tablename__ = "recipe_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    recipe_name = Column(
        String,
        nullable=False
    )

    ingredients = Column(
        String,
        nullable=False
    )


Base.metadata.create_all(
    bind=engine
)