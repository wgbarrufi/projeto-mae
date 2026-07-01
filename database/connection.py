from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine(
    "sqlite:///copa2026.db"
)

SessionLocal = sessionmaker(
    bind=engine
)