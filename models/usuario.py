from datetime import date


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

    def __init__(self, nome: str, email: str, cpf: str, dataNascimento: date, login: str, senha: str):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.dataNascimento = dataNascimento
        self.login = login
        self.senha = senha
        self.pontos = 100
        self.status = "Ativo"
        self.acertos = 0
        