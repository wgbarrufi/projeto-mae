from database.connection import engine

from models.base import Base
from models.usuario import Usuario

Base.metadata.create_all(engine)

print("Banco criado!")