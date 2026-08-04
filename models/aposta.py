from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.usuario import Usuario
    from models.partida import Partida

from sqlmodel import SQLModel, Field, Relationship

from models.status_aposta import StatusAposta


class Aposta(SQLModel, table=True):
    __tablename__ = "apostas"

    id: Optional[int] = Field(default=None, primary_key=True)

    usuario_id: int = Field(foreign_key="usuarios.id")
    partida_id: int = Field(foreign_key="partidas.id")

    palpite: str

    odd: float

    valor_pontos: float

    multiplicador: int = 1

    status: StatusAposta = StatusAposta.PENDENTE

    data_aposta: datetime = Field(default_factory=datetime.now)

    usuario: Optional["Usuario"] = Relationship(back_populates="apostas")

    partida: Optional["Partida"] = Relationship(back_populates="apostas")