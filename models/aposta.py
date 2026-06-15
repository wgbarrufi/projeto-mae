from models.partida import Partida

class Aposta():
    partida: Partida
    odd: float
    palpite: str
    

    def __init__(self, partida: Partida, odd: float, palpite: str):
        self.partida = partida
        self.odd = odd
        self.palpite = palpite