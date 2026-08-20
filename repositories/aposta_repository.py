from sqlmodel import Session, select
from database.connection import engine
from database.session import get_session
from models.aposta import Aposta
from sqlalchemy.orm import selectinload

class ApostaRepository:
    """
    Camada de acesso aos dados das apostas.

    Centraliza operações de consulta, inserção e atualização
    utilizando SQLModel e SQLite.
    """

    def salvar(self, aposta: Aposta):

        with get_session() as session:

            session.add(aposta)

            session.commit()

            session.refresh(aposta)

            return aposta

    def listar(self):

        with get_session() as session:

            statement = select(Aposta)

            return session.exec(statement).all()

    def buscar_por_usuario_e_partida(self,usuario_id: int,partida_id: int):

        with Session(engine) as session:

            return session.exec(
                select(Aposta).where(
                    Aposta.usuario_id == usuario_id,
                    Aposta.partida_id == partida_id
                )
            ).first()
        
    def buscar_por_id(self, aposta_id: int):

        with get_session() as session:

            return session.get(Aposta, aposta_id)
        
    def listar_por_usuario(self, usuario_id):
        with get_session() as session:

            statement = (
                select(Aposta)
                .options(selectinload(Aposta.partida))
                .where(Aposta.usuario_id == usuario_id)
            )

            return session.exec(statement).all()
        
    def listar_por_partida(self, partida_id):

        with get_session() as session:

            statement = (
                select(Aposta)
                .options(
                    selectinload(Aposta.usuario),
                    selectinload(Aposta.partida)
                )
                .where(
                    Aposta.partida_id == partida_id
                )
            )

            return session.exec(statement).all()

    def atualizar(self, aposta):

        with get_session() as session:

            session.add(aposta)

            session.commit()

            session.refresh(aposta)

            return aposta