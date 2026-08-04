from sqlmodel import create_engine

DATABASE_URL = "sqlite:///copa2026.db"

engine = create_engine(
    DATABASE_URL,
    echo=True
)