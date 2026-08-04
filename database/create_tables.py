from sqlmodel import SQLModel
from database.connection import engine

# Importar os modelos para que sejam registrados no metadata
from models.usuario import Usuario
from models.partida import Partida
from models.aposta import Aposta

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    print("Banco criado!")