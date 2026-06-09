from datetime import datetime


class Partida():
    timeCasa: str
    timeVisitante: str
    dataHora: datetime
    status: str
    resultado: int

    def __init__(self, timeCasa: str, timeVisitante: str, dataHora: datetime):
        self.timeCasa = timeCasa
        self.timeVisitante = timeVisitante
        self.dataHora = dataHora
        self.status = "Pendente"
        self.resultado = 0
        