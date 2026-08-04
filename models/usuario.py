from datetime import date
from typing import Optional, List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from models.status_usuario import StatusUsuario
from models.tipo_usuario import TipoUsuario

if TYPE_CHECKING:
    from models.aposta import Aposta


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)

    nome: str
    email: str = Field(unique=True)
    cpf: str = Field(unique=True)

    dataNascimento: date

    login: str = Field(unique=True)
    senha: str

    pontos: int = 100
    acertos: int = 0

    status: StatusUsuario = StatusUsuario.ATIVO
    tipo: TipoUsuario = TipoUsuario.USUARIO

    apostas: List["Aposta"] = Relationship(back_populates="usuario")