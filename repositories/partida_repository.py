from typing import Optional

from sqlmodel import select

from database.session import get_session
from models.partida import Partida

from datetime import datetime
from sqlmodel import select

class PartidaRepository:

    def salvar(self, partida: Partida) -> Partida:
        with get_session() as session:
            session.add(partida)
            session.commit()
            session.refresh(partida)
            return partida

    def buscar_por_id(self, partida_id: int) -> Optional[Partida]:
        with get_session() as session:
            return session.get(Partida, partida_id)

    def buscar_por_api_id(self, api_id: int) -> Optional[Partida]:
        with get_session() as session:
            statement = select(Partida).where(Partida.api_id == api_id)
            return session.exec(statement).first()

    def listar(self) -> list[Partida]:
        with get_session() as session:
            statement = select(Partida)
            return session.exec(statement).all()

    def atualizar(self, partida: Partida) -> Partida:
        with get_session() as session:
            session.add(partida)
            session.commit()
            session.refresh(partida)
            return partida

    def listar_disponiveis(self):
        with get_session() as session:

            agora = datetime.now()

            statement = select(Partida).where(
                Partida.encerrada == False,
                Partida.data_hora > agora
            )

            return session.exec(statement).all()