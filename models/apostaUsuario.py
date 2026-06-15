from datetime import datetime
from models.aposta import Aposta
from models.usuario import Usuario
from statusAposta import StatusAposta

class ApostaUsuario:
    usuario: Usuario
    aposta: Aposta
    valorPontos: float
    multiplicador: float
    status: str
    dataAposta: datetime

    def __init__(self, usuario: Usuario, aposta: Aposta, valorPontos: float):
        self.usuario = usuario
        self.aposta = aposta
        self.valorPontos = valorPontos
        self.multiplicador = 1
        self.status = StatusAposta.PENDENTE
        self.dataAposta = datetime.now()