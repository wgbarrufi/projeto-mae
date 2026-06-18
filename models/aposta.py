from datetime import datetime

from models.partida import Partida
from models.usuario import Usuario
from statusAposta import StatusAposta


class Aposta:

    def __init__(self, usuario: Usuario, partida: Partida, palpite: str, odd: float, valorPontos: float):
        self.usuario = usuario
        self.partida = partida
        self.palpite = palpite
        self.odd = odd
        self.valorPontos = valorPontos
        self.multiplicador = 1
        self.status = StatusAposta.PENDENTE
        self.dataAposta = datetime.now()

        
