from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "sqlite:///copa2026.db"
)

SessionLocal = sessionmaker(
    bind=engine
)