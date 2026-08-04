from typing import Optional, List, TYPE_CHECKING
if TYPE_CHECKING:
    from models.aposta import Aposta
from sqlmodel import Relationship

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Partida(SQLModel, table=True):
    __tablename__ = "partidas"

    id: Optional[int] = Field(default=None, primary_key=True)

    api_id: Optional[int] = Field(default=None, unique=True)

    time_casa: str
    time_visitante: str

    data_hora: datetime

    odd_casa: float
    odd_empate: float
    odd_visitante: float

    gols_casa: int = 0
    gols_visitante: int = 0

    encerrada: bool = False

    apostas: List["Aposta"] = Relationship(back_populates="partida")