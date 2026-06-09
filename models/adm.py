from datetime import datetime
from .usuario import Usuario

class Adm(Usuario):
    def __init__(self, nome: str, email: str, cpf: str, dataNascimento: datetime, login: str, senha: str):
        super().__init__(nome, email, cpf, dataNascimento, login, senha)
        self.acertos = 0