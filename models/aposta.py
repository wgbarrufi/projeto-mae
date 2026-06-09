from models.partida import Partida

class Aposta():
    partida: Partida
    odd: float
    status: str

    def __init__(self, partida: Partida, odd: float):
        self.partida = partida
        self.odd = odd
        self.status = "Pendente"