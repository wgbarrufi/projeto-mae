from typing import Optional

from database.session import get_session
from models.usuario import Usuario

from sqlmodel import Session, select

from database.connection import engine
from models.usuario import Usuario

class UsuarioRepository:
    """
    Camada de acesso aos dados dos usuários.
    """

    def salvar(self, usuario: Usuario) -> Usuario:
        with get_session() as session:
            session.add(usuario)
            session.commit()
            session.refresh(usuario)
            return usuario

    def buscar_por_id(self, usuario_id: int) -> Optional[Usuario]:
        with get_session() as session:
            return session.get(Usuario, usuario_id)

    def buscar_por_cpf(self, cpf: str) -> Optional[Usuario]:
        with get_session() as session:
            statement = select(Usuario).where(Usuario.cpf == cpf)
            return session.exec(statement).first()

    def buscar_por_login(self, login: str) -> Optional[Usuario]:
        with get_session() as session:
            statement = select(Usuario).where(Usuario.login == login)
            return session.exec(statement).first()

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        with get_session() as session:
            statement = select(Usuario).where(Usuario.email == email)
            return session.exec(statement).first()

    def listar(self) -> list[Usuario]:
        with get_session() as session:
            statement = select(Usuario)
            return session.exec(statement).all()

    def atualizar(self, usuario: Usuario) -> Usuario:
        with get_session() as session:
            session.add(usuario)
            session.commit()
            session.refresh(usuario)
            return usuario

    def excluir(self, usuario: Usuario) -> None:
        with get_session() as session:
            session.delete(usuario)
            session.commit()

    def ranking(self):
        with Session(engine) as session:

            usuarios = session.exec(
                select(Usuario).order_by(
                    Usuario.acertos.desc(),
                    Usuario.pontos.desc()
                )
            ).all()

            return usuarios