from models.usuario import Usuario


class Ranking:
    posicao: int
    usuario: Usuario
    acertos: int
    pontos: int

    def __init__(self, posicao: int, usuario: Usuario):
        self.posicao = posicao
        self.usuario = usuario
        self.acertos = usuario.acertos
        self.pontos = usuario.pontos