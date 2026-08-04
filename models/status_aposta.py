from enum import Enum

class StatusAposta(str, Enum):
    PENDENTE = "PENDENTE"
    GANHOU = "GANHOU"
    PERDEU = "PERDEU"
    EMPATE = "EMPATE"