from datetime import datetime
from statusAposta import StatusAposta

class Partida():
    timeCasa: str
    timeVisitante: str
    dataHora: datetime
    status: str
    golsCasa: int
    golsVisitante: int

    def __init__(self, timeCasa: str, timeVisitante: str, dataHora: datetime):
        self.timeCasa = timeCasa
        self.timeVisitante = timeVisitante
        self.dataHora = dataHora
        self.status = StatusAposta.PENDENTE
        self.resultado = 0
        self.golsCasa = 0
        self.golsVisitante = 0
        