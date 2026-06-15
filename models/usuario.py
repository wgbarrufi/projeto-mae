from datetime import date
from statusAposta import StatusAposta


class Usuario:
    nome: str
    email: str
    cpf: str
    dataNascimento: date
    login: str
    senha: str
    pontos: int
    status: str
    acertos: int
    tipo: str

    def __init__(self, nome: str, email: str, cpf: str, dataNascimento: date, login: str, senha: str, tipo: str = "USUARIO"):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.dataNascimento = dataNascimento
        self.login = login
        self.senha = senha
        self.pontos = 100
        self.status = StatusAposta.ATIVO
        self.acertos = 0
        self.tipo = tipo
        